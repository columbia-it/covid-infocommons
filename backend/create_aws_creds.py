#!/usr/bin/env python

import boto3
import configparser
import os
from pathlib import Path
import sys


DEFAULT_DURATION_SECONDS = 900
AWS_REGION = 'us-east-1'
AWS_ROLE = 'cuit-dev-role'
AWS_ALIAS = "default"


def get_credentials(cred_duration):
    """
    Retrieves AWS access key, secret access key, and session token
    """
    aws_account = os.getenv('CIC_AWS_ACCOUNT')
    aws_role = os.getenv('CIC_AWS_ROLE', AWS_ROLE)
    aws_id = os.getenv('CIC_AWS_ID')
    aws_key = os.getenv('CIC_AWS_KEY')
    if not (aws_account or aws_id or aws_key):
        raise Exception('AWS account or service ID or service key is not provided')
    role_arn = f'arn:aws:iam::{aws_account}:role/{aws_role}'
    client = boto3.Session(aws_access_key_id=aws_id, aws_secret_access_key=aws_key).client('sts')
    role = client.assume_role(RoleArn=role_arn, RoleSessionName='ACS-switch-role', DurationSeconds=cred_duration)
    return role['Credentials']


def write_credentials(credentials, aws_alias, aws_region):
    """
    Reads the existing file for AWS credentials and updates it for the given alias
    """
    homedir = str(Path.home())
    aws_credentials_path = os.path.join(homedir, '.aws/credentials')
    aws_credentials = configparser.ConfigParser()
    aws_credentials.read(aws_credentials_path)
    
    aws_credentials[aws_alias] = {}
    aws_credentials[aws_alias]['aws_access_key_id'] = credentials['AccessKeyId']
    aws_credentials[aws_alias]['aws_secret_access_key'] = credentials['SecretAccessKey']
    aws_credentials[aws_alias]['aws_session_token'] = credentials['SessionToken']
    aws_credentials[aws_alias]['region'] = aws_region
    
    with open(aws_credentials_path, 'w') as configfile:
        aws_credentials.write(configfile)


def main():
    """
    Retrieves AWS credentials and writes it to a home directory
    """
    cred_duration = DEFAULT_DURATION_SECONDS
    if len(sys.argv) >= 2:
        cred_duration = int(sys.argv[1])
    credentials = get_credentials(cred_duration)
    if not credentials:
        raise Exception('Failed to get AWS credentials')
    aws_alias = os.getenv('CIC_AWS_ALIAS', AWS_ALIAS)
    aws_region = os.getenv('CIC_AWS_REGION', AWS_REGION)
    write_credentials(credentials, aws_alias, aws_region)


if __name__ == '__main__':
    main()