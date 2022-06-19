from datetime import date, datetime
import cic_grants
import cic_orgs
import cic_people
import json
import logging
import requests


NSF_GRANT_REQUEST = "https://api.nsf.gov/services/v1/awards.json?keyword=covid+covid-19+corid-19+corvid-19+coronavirus+sars2+%22SARS-CoV-2%22&printFields=abstractText,agency,awardAgencyCode,awardee,awardeeAddress,awardeeCity,awardeeCountryCode,awardeeCounty,awardeeDistrictCode,awardeeName,awardeeStateCode,awardeeZipCode,cfdaNumber,coPDPI,date,dunsNumber,estimatedTotalAmt,expDate,fundAgencyCode,fundProgramName,fundsObligatedAmt,id,offset,parentDunsNumber,pdPIName,perfAddress,perfCity,perfCountryCode,perfCounty,perfDistrictCode,perfLocation,perfStateCode,perfZipCode,piEmail,piFirstName,piLastName,piMiddeInitial,piPhone,poEmail,poName,poPhone,primaryProgram,projectOutComesReport,publicationConference,publicationResearch,rpp,startDate,title,transType"

NSF_SINGLE_GRANT_REQUEST = "https://api.nsf.gov/services/v1/awards.json?printFields=abstractText,agency,awardAgencyCode,awardee,awardeeAddress,awardeeCity,awardeeCountryCode,awardeeCounty,awardeeDistrictCode,awardeeName,awardeeStateCode,awardeeZipCode,cfdaNumber,coPDPI,date,dunsNumber,estimatedTotalAmt,expDate,fundAgencyCode,fundProgramName,fundsObligatedAmt,id,offset,parentDunsNumber,pdPIName,perfAddress,perfCity,perfCountryCode,perfCounty,perfDistrictCode,perfLocation,perfStateCode,perfZipCode,piEmail,piFirstName,piLastName,piMiddeInitial,piPhone,poEmail,poName,poPhone,primaryProgram,projectOutComesReport,publicationConference,publicationResearch,rpp,startDate,title,transType&id="

SKIP_EXISTING = True

DIRECTORATES = [
'Biological Sciences (BIO)',
'Computer and Information Science and Engineering (CISE)',
'Education and Human Resources (EHR)',
'Engineering (ENG)',
'Environmental Research and Education (ERE)',
'Geosciences (GEO)',
'Mathematical and Physical Sciences (MPS)',
'Social, Behavioral, and Economic Sciences (SBE)',
'Technology, Innovation and Partnerships (TIP)',
'Office of the Director'
]

DIVISION_TO_DIRECTORATE = {
    'Science of Science': 'Social, Behavioral, and Economic Sciences (SBE)',
    'Tribal College & Univers Prog': 'Education and Human Resources (EHR)',
    'CONDENSED MATTER & MAT THEORY': 'Mathematical and Physical Sciences (MPS)',
    'SoO-Science Of Organizations': 'Social, Behavioral, and Economic Sciences (SBE)',
    'Plant Genome Research Resource': 'Biological Sciences (BIO)',
    'ERI-Eng. Research Initiation': 'Engineering (ENG)',
    'TOPOLOGY': 'Mathematical and Physical Sciences (MPS)',
    'AIB-Acctble Institutions&Behav': 'Social, Behavioral, and Economic Sciences (SBE)',
    'SHIPBOARD SCIENTIFIC SUPP EQUI': 'Geosciences (GEO)',
    'CDS&E-MSS': 'Mathematical and Physical Sciences (MPS)',
    'CA-HDR: Convergence Accelerato': 'Technology, Innovation and Partnerships (TIP)',
    'BIOSENS-Biosensing': 'Engineering (ENG)',
    'Comm & Information Foundations': 'Computer and Information Science and Engineering (CISE)',
    'Cultural Anthropology': 'Social, Behavioral, and Economic Sciences (SBE)',
    'Data Cyberinfrastructure': 'Computer and Information Science and Engineering (CISE)',
    'Decision, Risk & Mgmt Sci': 'Engineering (ENG)',
    'Discovery Research K-12': 'Education and Human Resources (EHR)',
    'Ecology of Infectious Diseases': 'Biological Sciences (BIO)',
    'FD-Fluid Dynamics': 'Engineering (ENG)',
    'I-Corps': 'Technology, Innovation and Partnerships (TIP)',
    'Info Integration & Informatics': 'Computer and Information Science and Engineering (CISE)',
    'MATHEMATICAL BIOLOGY': 'Mathematical and Physical Sciences (MPS)',
    'Nanoscale Interactions Program': 'Engineering (ENG)',
    'Sociology': 'Social, Behavioral, and Economic Sciences (SBE)',
    'CIS-Civil Infrastructure Syst': 'Engineering (ENG)',
    'Secure &Trustworthy Cyberspace': 'Computer and Information Science and Engineering (CISE)',
    'EPSCoR RII Track-4: Res Fellow': 'Office of the Director',
    'SBIR Phase II': 'Technology, Innovation and Partnerships (TIP)',
    'Software & Hardware Foundation': 'Computer and Information Science and Engineering (CISE)',
    'PHYSICS OF LIVING SYSTEMS': 'Mathematical and Physical Sciences (MPS)',
    'Systems and Synthetic Biology': 'Biological Sciences (BIO)',
    'STATISTICS': 'Mathematical and Physical Sciences (MPS)',
    'SBIR Phase I': 'Technology, Innovation and Partnerships (TIP)',
    'Genetic Mechanisms': 'Biological Sciences (BIO)',
    'STTR Phase I': 'Technology, Innovation and Partnerships (TIP)',
    'Robert Noyce Scholarship Pgm': 'Education and Human Resources (EHR)',
    'Fairness in Artificial Intelli': 'Computer and Information Science and Engineering (CISE)',
    'HCC-Human-Centered Computing': 'Computer and Information Science and Engineering (CISE)',
    'RSCH EXPER FOR UNDERGRAD SITES': 'Computer and Information Science and Engineering (CISE)',
    'Law & Science': 'Social, Behavioral, and Economic Sciences (SBE)',
    'OCEANOGRAPHIC INSTRUMENTATION': 'Geosciences (GEO)',
    'zzzzzz': 'zzzzzz'
}

def main():
    max_year = date.today().year + 1
    imported_count = 0

    # The NSF API will only return a max of 3000 grants per request, and the default page size is 25
    # So we request one month at a time, and step through each page
    for year in range(max_year, 2005, -1):
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

                
def retrieve_single_nsf_grant(grant_id):
    nsf_url = f"{NSF_SINGLE_GRANT_REQUEST}{grant_id}"

    logging.info("Reading from NSF API")
    logging.info(f"REQUEST = {nsf_url}")

    response = requests.get(nsf_url)
    response_json = response.json()    
    grant = response_json['response']['award'][0]
    return grant
        
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
                "funder_divisions": nsf_divisions(grant),
                "program_reference_codes": [],
                "keywords": [],
                "program_officials": nsf_program_official(grant),
                "other_investigators": nsf_other_investigators(grant),
                "principal_investigator": nsf_principal_investigator(grant),
                "funder": {
                    "type": "Funder",
                    "id": 3 # TODO -- this should be looked up!
                },
                "awardee_organization": nsf_awardee_org(grant),
                "award_id": grant['id'],
                "title": grant['title'],
                "start_date": nsf_to_cic_date(grant['startDate']),
                "end_date": nsf_to_cic_date(grant['expDate']),
                "award_amount": nsf_award_amount(grant),
                "abstract": grant['abstractText']
            }
        }
    }
    return grant_data


def nsf_divisions(grant):
    divisions = []
    if 'fundProgramName' not in grant:
        return divisions

    divisions.append(grant['fundProgramName'])

    # if the program name is in the lookup table, add the directorate name
    directorate = DIVISION_TO_DIRECTORATE[grant['fundProgramName']]
    if directorate is not None:
        divisions.insert(0,directorate)
    
    return divisions


def nsf_program_official(grant):
    # TODO -- incorporate the grant['poEmail'] into any person that is created
    # Turn the person into a reference like
    #  {
    #    "type": "Person",
    #    "id": "1"
    #  }
    if 'poName' not in grant:
        return []
    name = grant['poName']
    last_space = name.rfind(" ")
    last = name[last_space+1:]
    first = name[:last_space]
    person = cic_people.find_or_create_person(first,last)
    if person is None:
        return []
    return [ { "type": "Person",
               "id": int(person['id']) } ]


def nsf_principal_investigator(grant):
    # TODO -- incorporate the email into any person that is created
    # Turn the person into a reference like
    #  {
    #    "type": "Person",
    #    "id": "1"
    #  }
    first = grant['piFirstName']
    last = grant['piLastName']
    # TODO 128 grant['piEmail']
    person = cic_people.find_or_create_person(first,last)
    if person is None:
        return None
    return { "type": "Person",
             "id": int(person['id']) }


def nsf_other_investigators(grant):
    # TODO -- incorporate the email into any person that is created
    # Turn the person into a reference like
    #  {
    #    "type": "Person",
    #    "id": "1"
    #  }

    other_investigators = []
    
    # NSF just puts the full name in a single field
    for fullname in grant['coPDPI']:
        fullsplit = fullname.rsplit(" ", 1)
        first = fullsplit[0]
        last = fullsplit[1]
        person = cic_people.find_or_create_person(first,last)
        if person is not None:
            other_investigators.append( { "type": "Person",
                                          "id": int(person['id']) } )
    return other_investigators


def nsf_awardee_org(grant):
    #  {
    #    "type": "Organization",
    #    "id": 24
    #   }
    if 'awardeeName' not in grant:
        return None
    name = grant['awardeeName']

    if 'awardeeCountryCode' not in grant:
        country_code = 'US'
    else:
        country_code = grant['awardeeCountryCode']

    if 'awardeeStateCode' not in grant:
        state_code = None
    else:
        state_code = grant['awardeeStateCode']
        
    org = cic_orgs.find_or_create_org(name, country_code, state_code)
    org_json = { "type": "Organization",
                 "id": int(org['id']) }
    logging.debug(f" -- attaching organization {org_json}")
    return org_json


def nsf_to_cic_date(d):
    parsed = datetime.strptime(d, "%m/%d/%Y")
    iso = parsed.strftime("%Y-%m-%d")
    return iso


def nsf_award_amount(grant):
    if 'estimatedTotalAmt' not in grant:
        return 0
    else:
        return grant['estimatedTotalAmt']
    

if __name__ == "__main__":
    main()
