from datetime import date, datetime
import cic_grants
import cic_orgs
import cic_people
import json
import logging
import requests

NIH_BASE = "https://api.reporter.nih.gov/v1/projects/Search"

STOP_LIMIT = 100000
SKIP_EXISTING = False

# Documentation for NIH grants API: https://api.reporter.nih.gov/?urls.primaryName=V2.0

def main():    
    max_year = date.today().year + 1
    imported_count = 0

    # process a single grant for debugging purposes
    #g = retrieve_nih_grant('3R01DK118222-03S1')
    #process_grant(g)
    #return

    print("NIH Harvester")
    
    # The NIH API will only return a max of 500 grants per request, and the default page size is 25 
    # So we request one month at a time, and step through each page
    for year in range(max_year, 2019, -1):
        print(f'==================== Imported so far: {imported_count} ==========================')
        print(f'==================== Retrieving {year} ======================')
            
        for offset in range(0, 5000, 25):
            grants = retrieve_nih_grants(year, offset)                
            if grants is None or len(grants) == 0:
                break
            print("")
            print(f"Received {len(grants)} grants, offset {offset}")
            for g in grants:
                process_grant(g)
            imported_count += len(grants)
            if imported_count >= STOP_LIMIT:
                return

                
def retrieve_nih_grant(award_id):
    criteria = nih_award_id_criteria(award_id)    
    response = requests.post(url = NIH_BASE,
                             data = json.dumps(criteria),
                             headers={"Content-Type":"application/vnd.api+json"})
    response_json = response.json()
    grants = response_json['results']
    logging.info(f"retrieved grant {grants[0]}")
    return grants[0]
    

def retrieve_nih_grants(year, offset):
    logging.info("Reading grants from NIH API")
    criteria = nih_covid_query_criteria(year, offset)
    
    response = requests.post(url = NIH_BASE,
                             data = json.dumps(criteria),
                             headers={"Content-Type":"application/vnd.api+json"})
    if response.status_code >= 300:
        logging.error(f"{response} {response.text}")
        print(f"ERROR {response} {response.text}")
        return []
    response_json = response.json()
    grants = response_json['results']
    return grants


def nih_covid_query_criteria(year,offset):
    c =  {
        "criteria":
        {
            "fiscal_years":[ year ],
            "covid_response": ["Reg-CV", "CV"]
        },
        "include_fields": [
            "ProjectTitle", "AbstractText", "FiscalYear",
            "Organization", "OrgCountry", "OrgName",
            "ProjectNum", "ProjectNumSplit",
            "ContactPiName","PrincipalInvestigators","ProgramOfficers",
            "ProjectStartDate","ProjectEndDate",
            "AwardAmount", "AgencyIcFundings", "PrefTerms",
        ],
        "offset": offset,
        "limit":25
    }
    return c


def nih_award_id_criteria(award_id):
    c =  {
        "criteria":
        {
            "project_nums": [award_id]
        },
        "include_fields": [
            "ProjectTitle", "AbstractText", "FiscalYear",
            "Organization", "OrgCountry", "OrgName",
            "ProjectNum", "ProjectNumSplit",
            "ContactPiName","PrincipalInvestigators","ProgramOfficers",
            "ProjectStartDate","ProjectEndDate",
            "AwardAmount", "AgencyIcFundings", "PrefTerms",
        ],
        "offset": 0,
        "limit":25
    }
    return c


def process_grant(grant):
    logging.info("======================================================================")
    logging.info(f" -- processing grant {grant['project_num']} -- {grant['project_title']}")
    logging.debug(grant)
    
    existing_grant = cic_grants.find_cic_grant(grant['project_num'])
    if existing_grant is None:        
        logging.debug("   -- not found - creating")
        grant_json = nih_to_cic_format(grant)
        response_code = cic_grants.create_cic_grant(grant_json)
    else:
        if SKIP_EXISTING:
            logging.debug("  -- found existing grant! skipping due to SKIP_EXISTING setting")
            return
        logging.debug("   -- found existing grant! updating")
        grant_json = nih_to_cic_format(grant)
        response_code = cic_grants.update_cic_grant(grant_json, existing_grant['id'])

    logging.info(f"    -- {response_code}")

    
def nih_to_cic_format(grant):
    grant_data = {
        "data": {
            "type": "Grant", 
            "attributes": {
                "funder_divisions": nih_funding_divisions(grant['agency_ic_fundings']),
                "keywords": nih_keywords(grant['pref_terms']),
                "program_officials": nih_program_officials(grant['program_officers']),
                "principal_investigator": nih_principal_investigator(grant),
                "other_investigators": nih_other_investigators(grant),
                "funder": {
                    "type": "Funder",
                    "id": 4 # TODO -- this should be looked up!
                },
                "awardee_organization": nih_awardee_org(grant['org_name'],grant['org_country']),
                "award_id": grant['project_num'],
                "title": grant['project_title'],
                "start_date": nih_to_cic_date(grant['project_start_date']),
                "end_date": nih_to_cic_date(grant['project_end_date']),
                "award_amount": grant['award_amount'],
                "abstract": nih_abstract(grant['abstract_text'])
            }
        }
    }
    return grant_data


def nih_abstract(text):
    if text is None:
        return
    
    # Remove errant \n put in by NIH API
    text = text.replace('\n', ' ')

    # remove annoying prefix markers
    bad_prefixes = ['other project information – ',
                    'project summary/abstract ',
                    'project summary ',
                    'project abstract ',
                    'abstract ',
                    'summary ']
    for p in bad_prefixes:
        plen = len(p)
        if text[0:plen].lower() == p.lower():
            text = text[plen:]

    return text


def nih_awardee_org(name, country):
    #  {
    #    "type": "Organization",
    #    "id": 24
    #   }    
    org = cic_orgs.find_or_create_org(name, country)
    org_json = { "type": "Organization",
                 "id": int(org['id']) }
    logging.debug(f" -- attaching organization {org_json}")
    return org_json


def nih_principal_investigator(grant):
    # Create the appropriate people, then return them as an array of references like
    #  {
    #    "type": "Person",
    #    "id": "1"
    #  }
    if 'principal_investigators' not in grant:
        return None
    people = grant['principal_investigators']
    first = people[0]['first_name']
    if len(people[0]['middle_name']) > 0:
        first += ' ' + people[0]['middle_name']
    last = people[0]['last_name']

    person = cic_people.find_or_create_person(first,last)
    if person is None:
        return None
    person_json = { "type": "Person",
                    "id": int(person['id']) }
    logging.debug(f" -- attaching person {person_json}")
    return person_json


def nih_other_investigators(grant):
    # Create the appropriate people, then return them as an array of references like
    #  {
    #    "type": "Person",
    #    "id": "1"
    #  }
    if 'principal_investigators' not in grant:
        return None
    people = grant['principal_investigators'][1:] #exclude the first investigator
    person_json = []
    for p in people:
        first = p['first_name']
        if len(p['middle_name']) > 0:
            first += ' ' + p['middle_name']
        last = p['last_name']

        person = cic_people.find_or_create_person(first,last)
        if person is None:
            return None
        logging.debug(f" -- attaching person {person}")
        person_json.append({ "type": "Person",
                             "id": int(person['id']) })
    return person_json


def nih_program_officials(grant_officials):
    # Create the appropriate people, then return them as an array of references like
    #  {
    #    "type": "Person",
    #    "id": "1"
    #  }
    first = grant_officials[0]['first_name']
    if len(grant_officials[0]['middle_name']) > 0:
        first += ' ' + grant_officials[0]['middle_name']
    last = grant_officials[0]['last_name']

    person = cic_people.find_or_create_person(first,last)
    if person is None:
        return []
    return [ { "type": "Person",
               "id": int(person['id']) } ]


def nih_keywords(s):
    if(s is None or len(s) == 0):
        return []
    else:
        s = s[0:1999] # some NIH grants have a staggering amount of keywords
        keys = s.split(';')
        keys = [i for i in keys if i]
        return keys

def nih_funding_divisions(ics):
    result = []
    for ic in ics:
        result.append(replace_commas(ic['name']))
    return result[0]


def replace_commas(s):
    return s.replace(",","\t")
    

def nih_to_cic_date(d):
    # ISO formatted as 2020-09-01T12:09:00Z, we strip the time for CIC
    t_index = d.index('T')
    iso = d[0:t_index]
    return iso

    

if __name__ == "__main__":
    main()
    
