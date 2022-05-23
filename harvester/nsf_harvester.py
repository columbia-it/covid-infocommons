from datetime import date, datetime
import cic_grants
import cic_orgs
import cic_people
import json
import logging
import requests


NSF_GRANT_REQUEST = "https://api.nsf.gov/services/v1/awards.json?keyword=covid+covid-19+corid-19+corvid-19+coronavirus+sars2+%22SARS-CoV-2%22&printFields=abstractText,agency,awardAgencyCode,awardee,awardeeAddress,awardeeCity,awardeeCountryCode,awardeeCounty,awardeeDistrictCode,awardeeName,awardeeStateCode,awardeeZipCode,cfdaNumber,coPDPI,date,dunsNumber,estimatedTotalAmt,expDate,fundAgencyCode,fundProgramName,fundsObligatedAmt,id,offset,parentDunsNumber,pdPIName,perfAddress,perfCity,perfCountryCode,perfCounty,perfDistrictCode,perfLocation,perfStateCode,perfZipCode,piEmail,piFirstName,piLastName,piMiddeInitial,piPhone,poEmail,poName,poPhone,primaryProgram,projectOutComesReport,publicationConference,publicationResearch,rpp,startDate,title,transType"
SKIP_EXISTING = True


def main():    
    max_year = date.today().year + 1
    imported_count = 0

    # The NSF API will only return a max of 3000 grants per request, and the default page size is 25
    # So we request one month at a time, and step through each page
    for year in range(2005, max_year):
        for month in range(1, 13):
            print(f'==================== Imported so far: {imported_count} ==========================')
            print(f'==================== Retrieving month {year}-{month} ======================')

            for offset in range(0, 3000, 25):
                grants = retrieve_nsf_grants(year, month, offset)                
                print(f"Received {len(grants)} grants")
                if len(grants) == 0:
                    break
                for g in grants:
                    process_grant(g)
                imported_count += len(grants)
        
        
def retrieve_nsf_grants(year, month, offset):
    if month < 10:
        monthstr = f'0{month}'
    else:
        monthstr = month
    monthfilter = f"&dateStart={monthstr}/01/{year}&dateEnd={monthstr}/31/{year}"

    nsf_url = f"{NSF_GRANT_REQUEST}{monthfilter}&offset={offset}"

    logging.info("Reading from NSF API")
    logging.info(f"REQUEST = {nsf_url}")

    response = requests.get(nsf_url)
    response_json = response.json()    
    grants = response_json['response']['award']
    return grants


def process_grant(grant):
    logging.info("======================================================================")
    logging.info(f" -- processing grant {grant['id']} -- {grant['title']}")

    existing_grant = cic_grants.find_cic_grant(grant['id'])
    if existing_grant is None:        
        logging.debug("   -- not found - creating")
        grant_json = nsf_to_cic_format(grant)
        response_code = cic_grants.create_cic_grant(grant_json)
    else:
        if SKIP_EXISTING:
            logging.debug("  -- found existing grant! skipping due to SKIP_EXISTING setting")
            return
        logging.debug("   -- found existing grant! updating")
        grant_json = nsf_to_cic_format(grant)
        response_code = cic_grants.update_cic_grant(grant_json, grant['id'])
        
    logging.info(f"    -- {response_code}")

    
def nsf_to_cic_format(grant):
    grant_data = {
        "data": {
            "type": "Grant", 
            "attributes": {
                "funder_divisions": [ grant['fundProgramName'] ],
                "program_reference_codes": [],
                "keywords": [],
                "program_officials": nsf_program_official(grant),
                "other_investigators": [ ],
                "principal_investigator": nsf_principal_investigator(grant['piFirstName'],grant['piLastName'],grant['piEmail']),
                "funder": {
                    "type": "Funder",
                    "id": 3 # TODO -- this should be looked up!
                },
                "awardee_organization": nsf_awardee_org(grant['awardeeName'], grant['awardeeCountryCode']),
                "award_id": grant['id'],
                "title": grant['title'],
                "start_date": nsf_to_cic_date(grant['startDate']),
                "end_date": nsf_to_cic_date(grant['expDate']),
                "award_amount": grant['estimatedTotalAmt'] or 0,
                "abstract": grant['abstractText']
            }
        }
    }
    return grant_data


def nsf_program_official(grant):
    # TODO -- incorporate the grant['poEmail'] into any person that is created
    # Turn the person into a reference like
    #  {
    #    "type": "Person",
    #    "id": "1"
    #  }
    if 'poName' not in grant:
        return None
    name = grant['poName']
    last_space = name.rfind(" ")
    last = name[last_space+1:]
    first = name[:last_space]
    person = cic_people.find_or_create_person(first,last)
    return [ { "type": "Person",
               "id": int(person['id']) } ]


def nsf_principal_investigator(first, last, email):
    # TODO -- incorporate the email into any person that is created
    # Turn the person into a reference like
    #  {
    #    "type": "Person",
    #    "id": "1"
    #  }
    person = cic_people.find_or_create_person(first,last)
    if person is None:
        return None
    return { "type": "Person",
             "id": int(person['id']) }


def nsf_awardee_org(name, country_code):
    #  {
    #    "type": "Organization",
    #    "id": 24
    #   }    
    org = cic_orgs.find_or_create_org(name, country_code)
    org_json = { "type": "Organization",
                 "id": int(org['id']) }
    logging.debug(f" -- attaching organization {org_json}")
    return org_json


def nsf_to_cic_date(d):
    parsed = datetime.strptime(d, "%m/%d/%Y")
    iso = parsed.strftime("%Y-%m-%d")
    return iso


if __name__ == "__main__":
    main()
