#!/usr/bin/env python3

"""
AWS helper script writtin in Python script to connect to CAS/Shibboleth
via Selenium/webdriver and retrieve a SAML manifest. SAML manifest is
saved locally to disk

By default, script then connects to AWS and retrieves STS credentials
for each account/role, and writes the output to a json file and ~/.aws/credentials

Based on work by Quint Van Deman, see https://aws.amazon.com/blogs/security/how-to-implement-federated-api-and-cli-access-using-saml-2-0-and-ad-fs/



usage: ./saml.py [aws role] [aws account id1 ...]

e.g.

    ./saml.py cuit-dev-role

to generate credentials for all accounts that your uni has under that role

or

    ./saml.py cuit-dev-role 025533440677 123328872028

for a specific account(s) (useful when different accounts have different SessionDuration)


Both of these optional. If run without arguments, generates api keys for all accounts found.

Instructions:
1. Download the appropriate chromedriver executable for your operating system from  https://sites.google.com/a/chromium.org/chromedriver/downloads
    - put the executable in $PATH, or %PATH% in windows.
    - https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/
2. pip install selenium boto3
    (use a venv if you want)

Options:
- pass `--hours <number of hours>` if you want more time (e.g. 12 hours). For this to be accepted, the IAM role is required to have at least that much time in its "max session duration"
- pass `--headless` if your Duo automatically pushes a notification
- If your Duo doesn't automatically push (it's in the duo settings) set headless to False so the duo window will be shown


Modified from
https://gitlab.cc.columbia.edu/cuit-infra-sys/aws-admin-tools/blob/master/saml.py

link: https://gitlab.cc.columbia.edu/snippets/64

"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import getpass
import time
import sys
import os
import xml.etree.ElementTree as ET
import base64
import configparser
import boto3
import botocore
import json
from pathlib import Path
import argparse

uri = 'https://shibboleth.columbia.edu/idp/profile/SAML2/Unsolicited/SSO?providerId=urn:amazon:webservices'

DEFAULT_REGION = 'us-east-1'


def get_homedir():
    return str(Path.home())


def write_credentials(creds, role=None):
    """ writes the credentials to the aws credentials file.
        If role is given, it only writes the credentials matching the role"""

    homedir = get_homedir()
    aws_credentials_path = os.path.join(homedir, '.aws/credentials')

    aws_credentials = configparser.ConfigParser()
    aws_credentials.read(aws_credentials_path)

    roles_written = 0

    for cred in creds:
        if role is not None and cred['role'] != role:
            continue
        alias = cred['alias']
        aws_credentials[alias] = {}
        aws_credentials[alias]['aws_access_key_id'] = cred['aws_access_key_id']
        aws_credentials[alias]['aws_secret_access_key'] = cred['aws_secret_access_key']
        aws_credentials[alias]['aws_session_token'] = cred['aws_session_token']
        aws_credentials[alias]['region'] = DEFAULT_REGION
        roles_written += 1
        print("writing profile", alias)

    with open(aws_credentials_path, 'w') as configfile:
        aws_credentials.write(configfile)

    return roles_written


def get_cached_assertion(assertionfname):
    # see if there's a cached assertion file
    try:
        ageok = time.time() - os.path.getmtime(assertionfname) < 300
    except FileNotFoundError:
        ageok = False

    assertion = None
    # if so, read that
    if ageok:
        print("using cached assertion from", assertionfname)
        with open(assertionfname, "r") as f:
            assertion = f.read()

    return assertion


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('role', nargs='?', help="the role to filter on")
    parser.add_argument('accountids', nargs='*', help="the accountid to filter on")
    parser.add_argument('--headless', action='store_true',
                        help="enable headless mode. Requires automatic DUO push to work")
    parser.add_argument('--hours', default=1, type=int, help="session duration in hours")
    parser.add_argument('-v', '--verbose', action='store_true', help="verbose mode")
    parser.add_argument('--cache-assertion', action='store_true', help="set to cache the saml assertion")

    args = parser.parse_args()

    filter_by_role = args.role
    if args.cache_assertion:
        assertionfname = os.path.join(get_homedir(), ".saml_assertion.tmp")
        assertion = get_cached_assertion(assertionfname)
    else:
        assertion = None

    if not assertion:
        if args.headless:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')

            driver = webdriver.Chrome(chrome_options=chrome_options)
            driver.get(uri)

            username = getpass.getuser()
            print("using user", username)
            password = getpass.getpass("Enter uni password: ")

            username_field = driver.find_element_by_name("username")
            username_field.clear()
            username_field.send_keys(username)

            password_field = driver.find_element_by_name("password")
            password_field.clear()
            password_field.send_keys(password)

            submit_button = driver.find_element_by_name("submit")
            submit_button.click()

            print("Sending a DUO Push")

        else:
            driver = webdriver.Chrome()
            driver.get(uri)

        element = WebDriverWait(driver, 90).until(
            EC.presence_of_element_located((webdriver.common.by.By.NAME, "SAMLResponse"))
        )

        assertion = element.get_attribute('value')

        driver.quit()

        if args.cache_assertion:
            with open(assertionfname, "w") as f:
                print("caching saml assertion in", assertionfname)
                f.write(assertion)

    # Parse the returned assertion and extract the authorized roles
    awsroles = []
    root = ET.fromstring(base64.b64decode(assertion))
    for saml2attribute in root.iter('{urn:oasis:names:tc:SAML:2.0:assertion}Attribute'):
        if (saml2attribute.get('Name') == 'https://aws.amazon.com/SAML/Attributes/Role'):
            for saml2attributevalue in saml2attribute.iter('{urn:oasis:names:tc:SAML:2.0:assertion}AttributeValue'):
                awsroles.append(saml2attributevalue.text)
                if args.verbose:
                    print("role: %s" % saml2attributevalue.text)

    # Note the format of the attribute value should be role_arn,principal_arn
    # but lots of blogs list it as principal_arn,role_arn so let's reverse
    # them if needed
    for awsrole in awsroles:
        chunks = awsrole.split(',')
        if 'saml-provider' in chunks[0]:
            newawsrole = chunks[1] + ',' + chunks[0]
            index = awsroles.index(awsrole)
            awsroles.insert(index, newawsrole)
            awsroles.remove(awsrole)

    awsroles.sort()

    credlist = list()
    # if False:
    for awsrole in awsroles:

        role_arn, principal_arn = awsrole.split(',')
        accid = role_arn.split(':')[4]
        rolename = role_arn.split(':')[5].split('/')[1]
        if len(accid) < 12:
            continue

        if filter_by_role is not None and rolename != filter_by_role:
            continue
        if len(args.accountids) > 0 and accid not in args.accountids:
            continue

        print(f"AccountID: {accid}, role: {rolename}", end='')

        client = boto3.client('sts')
        token = client.assume_role_with_saml(
            RoleArn=role_arn,
            PrincipalArn=principal_arn,
            SAMLAssertion=assertion,
            DurationSeconds=args.hours * 3600
        )

        sess = boto3.Session(
            aws_access_key_id=token['Credentials']['AccessKeyId'],
            aws_secret_access_key=token['Credentials']['SecretAccessKey'],
            aws_session_token=token['Credentials']['SessionToken'])

        iam = sess.client('iam')

        paginator = iam.get_paginator('list_account_aliases')
        aliases = list()
        try:
            for response in paginator.paginate():
                print(", aliases:", ",".join(response['AccountAliases']))
                aliases.extend(response['AccountAliases'])
        except botocore.exceptions.ClientError:
            print(", list_account_aliases denied")
            continue

        alias = "none"
        if len(aliases) > 0:
            alias = aliases[0]
        else:
            print("no alias?")

        credlist.append(
            {"accid": accid,
             "role": rolename,
             "alias": alias,
             "aws_access_key_id": str(token['Credentials']['AccessKeyId']),
             "aws_secret_access_key": str(token['Credentials']['SecretAccessKey']),
             "aws_session_token": str(token['Credentials']['SessionToken'])
             })

    """
    with open("stscreds.json","w") as f:
        json.dump(credlist,f)
    print('wrote creds to stscreds.json')
    """

    num_creds = write_credentials(credlist, filter_by_role)

    print('wrote {} credentials to ~/.aws/credentials'.format(num_creds))
