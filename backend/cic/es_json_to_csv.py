import pandas as pd
import json, requests 
import os

response = requests.get("https://cic-apps.datascience.columbia.edu/search/grants")
text = response.text
data = json.loads(text)
total_count = data['hits']['total']['value']
remaining_count = total_count
var_from = 0
print(remaining_count)
while remaining_count > 0:
    response = requests.get("https://cic-apps.datascience.columbia.edu/search/grants?from={}&size=1000".format(var_from))
    grants_data = json.loads(response.text)['hits']['hits']
    df = pd.json_normalize(grants_data)
    print(df.columns)
    df.drop(['_index','_type','_score','sort','_source.funder.id','_source.funder.ror','_source.funder_divisions','_source.program_reference_codes','_source.program_officials','_source.other_investigators','_source.principal_investigator.id','_source.principal_investigator.orcid','_source.principal_investigator.emails','_source.principal_investigator.private_emails','_source.principal_investigator.keywords','_source.principal_investigator.affiliations','_source.principal_investigator.last_name','_source.principal_investigator.first_name','_source.awardee_organization.id','_source.awardee_organization.ror','_source.awardee_organization.address','_source.awardee_organization.city','_source.awardee_organization.state','_source.awardee_organization.zip','_source.awardee_organization.country','_source.keywords','_source.start_date','_source.end_date'],  axis=1, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df['_source.award_amount'] = df['_source.award_amount'].apply(lambda x: "${:,.0f}".format(x))

    if not os.path.isfile('grants_2.csv'):
        df.to_csv('grants_2.csv', header='column_names', index=False)
    else: # else it exists so append without writing the header
        df.to_csv('grants_2.csv', mode='a', header=False, index=False)
    var_from = 1000 + var_from
    remaining_count = remaining_count - 1000
# df.drop(['type','attributes.funder.id','attributes.funder.ror','attributes.funder_divisions','attributes.program_reference_codes','attributes.program_officials','attributes.start_date','attributes.end_date','attributes.principal_investigator.id','attributes.principal_investigator.orcid','attributes.principal_investigator.emails','attributes.principal_investigator.private_emails','attributes.principal_investigator.keywords','attributes.principal_investigator.affiliations','attributes.other_investigators','attributes.awardee_organization.id','attributes.awardee_organization.ror','attributes.awardee_organization.address','attributes.awardee_organization.city','attributes.awardee_organization.state','attributes.awardee_organization.zip','attributes.awardee_organization.country','attributes.keywords']
# , axis=1, inplace=True)
