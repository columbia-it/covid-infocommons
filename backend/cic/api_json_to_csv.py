import pandas as pd
import json, requests 
import os


response = requests.get("https://cic-apps.datascience.columbia.edu/v1/grants")
more_data = True
text = response.text
data = json.loads(text)
grants_data = data['data']
df = pd.json_normalize(grants_data)
df.reset_index(drop=True, inplace=True)

df.drop(['type','attributes.funder.id','attributes.funder.ror','attributes.funder_divisions','attributes.program_reference_codes','attributes.program_officials','attributes.start_date','attributes.end_date','attributes.principal_investigator.id','attributes.principal_investigator.orcid','attributes.principal_investigator.emails','attributes.principal_investigator.private_emails','attributes.principal_investigator.keywords','attributes.principal_investigator.affiliations','attributes.other_investigators','attributes.awardee_organization.id','attributes.awardee_organization.ror','attributes.awardee_organization.address','attributes.awardee_organization.city','attributes.awardee_organization.state','attributes.awardee_organization.zip','attributes.awardee_organization.country','attributes.keywords']
, axis=1, inplace=True)

if not os.path.isfile('grants.csv'):
    df.to_csv('grants.csv', header='column_names', index=False)
else: # else it exists so append without writing the header
    df.to_csv('grants.csv', mode='a', header=False, index=False)
while more_data:
    print(data['links']['next'])
    if not data['links']['next']:
        more_data = False
        break
    response = requests.get(data['links']['next'])
    text = response.text
    data = json.loads(text)
    grants_data = data['data']
    df = pd.json_normalize(grants_data)
    #df.reset_index(drop=True, inplace=True)
    df.drop(['type','attributes.funder.id','attributes.funder.ror','attributes.funder_divisions','attributes.program_reference_codes','attributes.program_officials','attributes.start_date','attributes.end_date','attributes.principal_investigator.id','attributes.principal_investigator.orcid','attributes.principal_investigator.emails','attributes.principal_investigator.private_emails','attributes.principal_investigator.keywords','attributes.principal_investigator.affiliations','attributes.other_investigators','attributes.awardee_organization.id','attributes.awardee_organization.ror','attributes.awardee_organization.address','attributes.awardee_organization.city','attributes.awardee_organization.state','attributes.awardee_organization.zip','attributes.awardee_organization.country','attributes.keywords'],
     axis=1, inplace=True)
    if not os.path.isfile('grants.csv'):
        df.to_csv('grants.csv', header='column_names', index=False)
    else: # else it exists so append without writing the header
        df.to_csv('grants.csv', mode='a', header=False, index=False)

