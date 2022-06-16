from datetime import date, datetime
import cic_grants
import cic_orgs
import cic_people
import json
import logging
import requests

# Drupal Harvester -- Import grants and people from the CIC Drupal system


SKIP_EXISTING = False

def main():    
    grants = read_grants()
    for grant in grants:
        process(grant)
        exit

def process(grant):
    print(grant)
    drupal_to_cic_format(grant)
    # For each person, make a cic person

def read_grants():
    f = open('/home/ubuntu/cu_nsf_awards.json')
    # returns JSON object as 
    # a dictionary
    data = json.load(f)
    print(f"found {len(data)} grants")
    return data
    
    
def drupal_to_cic_format(grant):
    grant_data = {
        "data": {
            "type": "Grant", 
            "attributes": {
                "funder_divisions": drupal_divisions(grant),
                "program_reference_codes": #[],
                "keywords": #[],
                "program_officials": #nsf_program_official(grant),
                "other_investigators": drupal_other_investigators(grant),
                "principal_investigator": #nsf_principal_investigator(grant),
                "funder": {
                    "type": "Funder",
                    "id": 3 # TODO -- this should be looked up!
                },
                "awardee_organization": #nsf_awardee_org(grant),
                "award_id": grant['id'],
                "title": grant['title'],
                "start_date": grant['date'],
                "end_date": grant['expdate'],
                "award_amount": grant['fundsobligatedamt'],
                "abstract": grant['abstracttext']
            }
        }
    }
    return grant_data

DRUPAL_DIRECTORATE = {
'BIO - Directorate for Biological Sciences': 'Biological Sciences (BIO)',
'CSE - Directorate for Computer and Information Science and Engineering': 'Computer and Information Science and Engineering (CISE)',
'EHR - Directorate for Education and Human Resources': 'Education and Human Resources (EHR)',
'ENG - Directorate for Engineering': 'Engineering (ENG)',
'ERE - Environmental Research and Education': 'Environmental Research and Education (ERE)',
'GEO - Directorate for Geosciences': 'Geosciences (GEO)',
'MPS - Mathematical and Physical Sciences': 'Mathematical and Physical Sciences (MPS)',
'SBE - Social, Behavioral, and Economic Sciences': 'Social, Behavioral, and Economic Sciences (SBE)',
'TIP - Technology, Innovation and Partnerships': 'Technology, Innovation and Partnerships (TIP)',
'OD - Office of the Director''Office of the Director'
}

def drupal_divisions(grant):
    divisions = []

    if 'directorate' in grant:
        divisions.append(DRUPAL_DIRECTORATE[grant['directorate']])
    
    if 'fundProgramName' not in grant:
        return divisions

    divisions.append(grant['fundProgramName'])

    # if the program name is in the lookup table, add the directorate name
    directorate = DIVISION_TO_DIRECTORATE[grant['fundProgramName']]
    if directorate is not None:
        divisions.insert(0,directorate)
    
    return divisions


def drupal_other_investigators(grant):
    # Turn the person into a reference like
    #  {
    #    "type": "Person",
    #    "id": "1"
    #  }

    other_investigators = []
    
    # Drupal just puts the full name in a single field
    for fullname in grant['copdpi']:
        fullsplit = fullname.rsplit(" ", 1)
        first = fullsplit[0]
        last = fullsplit[1]
        person = cic_people.find_or_create_person(first,last)
        if person is not None:
            other_investigators.append( { "type": "Person",
                                          "id": int(person['id']) } )
    return other_investigators
    

if __name__ == "__main__":
    main()
