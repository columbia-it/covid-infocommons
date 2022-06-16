from datetime import date, datetime
import cic_grants
import cic_orgs
import cic_people
import json
import logging
import requests
import nsf_harvester

# Drupal Harvester -- Import grants and people from the CIC Drupal system

SKIP_EXISTING = True

def main():    
    grants = read_grants()
    print(f"found {len(grants)} grants")
    total = len(grants)
    processed = 0
    for grant in grants:
        process(grant)
        processed += 1
        if processed % 10 == 0:
            print(f"{processed}/{total}")


def process(grant):
    logging.info("======================================================================")
    logging.info(f" -- processing grant {grant['id']} -- {grant['title']}")
    existing_grant = cic_grants.find_cic_grant(grant['id'])
    if existing_grant is None:        
        logging.debug("   -- not found - creating")
        grant_json =  drupal_to_cic_format(grant)
        print(" pushing ")
        print(grant_json)
        response_code = cic_grants.create_cic_grant(grant_json)
    else:
        if SKIP_EXISTING:
            logging.debug("  -- found existing grant! skipping due to SKIP_EXISTING setting")
            return
        logging.debug("   -- found existing grant! updating")
        grant_json = drupal_to_cic_format(grant)
        response_code = cic_grants.update_cic_grant(grant_json, grant['id'])
        
    logging.info(f"    -- {response_code}")




def read_grants():
    f = open('/home/ubuntu/cu_nsf_awards.json')
    # returns JSON object as 
    # a dictionary
    data = json.load(f)
    return data
    
    
def drupal_to_cic_format(grant):
    grant_data = {
        "data": {
            "type": "Grant", 
            "attributes": {
                "funder_divisions": drupal_divisions(grant),
                "program_reference_codes": grant['programrefcodes'],
                "keywords": [],
                "program_officials": drupal_program_official(grant),
                "other_investigators": drupal_other_investigators(grant),
                "principal_investigator": drupal_principal_investigator(grant),
                "funder": {
                    "type": "Funder",
                    "id": 3 # TODO -- this should be looked up!
                },
                "awardee_organization": drupal_awardee_org(grant),
                "award_id": grant['id'],
                "title": grant['title'],
                "start_date": grant['startdate'],
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
'OD - Office of the Director': 'Office of the Director'
}

def drupal_divisions(grant):
    divisions = []
    if 'directorate' in grant:
        if len(grant['directorate']) > 0:
            divisions.append(DRUPAL_DIRECTORATE[grant['directorate']])
    
    # if the program name is in the lookup table, add the directorate name
    if len(divisions) == 0 and 'fundprogramname' in grant:
        if grant['fundprogramname'][0] in nsf_harvester.DIVISION_TO_DIRECTORATE:
            directorate = nsf_harvester.DIVISION_TO_DIRECTORATE[grant['fundprogramname'][0]]
            if directorate is not None:
                divisions.insert(0,directorate)

    if 'nsf_org' in grant and grant['nsf_org']:
        divisions.append(grant['nsf_org'])

    if 'fundprogramname' in grant:
        divisions.append(grant['fundprogramname'][0])
    
    return divisions


def drupal_awardee_org(grant):
    #  {
    #    "type": "Organization",
    #    "id": 24
    #   }
    if 'awardeename' not in grant:
        return None
    name = grant['awardeename']

    if 'awardeecountrycode' not in grant:
        country_code = 'US'
    else:
        country_code = grant['awardeecountrycode']

    if 'awardeestatecode' not in grant:
        state_code = None
    else:
        state_code = grant['awardeestatecode']
        
    org = cic_orgs.find_or_create_org(name, country_code, state_code)
    org_json = { "type": "Organization",
                 "id": int(org['id']) }
    logging.debug(f" -- attaching organization {org_json}")
    return org_json


def drupal_program_official(grant):
    # TODO -- incorporate the grant['poEmail'] into any person that is created
    # Turn the person into a reference like
    #  {
    #    "type": "Person",
    #    "id": "1"
    #  }
    if 'poname' not in grant:
        return []
    name = grant['poname']
    if not name:
        return []
    last_space = name.rfind(" ")
    last = name[last_space+1:]
    first = name[:last_space]
    person = cic_people.find_or_create_person(first,last)
    if person is None:
        return []
    return [ { "type": "Person",
               "id": int(person['id']) } ]


def drupal_principal_investigator(grant):
    # TODO -- incorporate the email into any person that is created
    # Turn the person into a reference like
    #  {
    #    "type": "Person",
    #    "id": "1"
    #  }

    fullsplit = grant['pdpiname'].rsplit(" ", 1)
    first = fullsplit[0]
    last = fullsplit[1]
    person = cic_people.find_or_create_person(first, last, grant['piemail'], grant['pilink'])
    if person is None:
        return None
    return { "type": "Person",
             "id": int(person['id']) }


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
