from datetime import date, datetime
import requests, json

CIC_BASE = "https://cice-dev.paas.cc.columbia.edu"
CIC_GRANTS_API = f"{CIC_BASE}/v1/grants"
CIC_PEOPLE_API = f"{CIC_BASE}/v1/people"
CIC_FUNDER_API = f"{CIC_BASE}/v1/funders"

NIH_BASE = "https://api.reporter.nih.gov/v1/projects/Search"

def main():    
    max_year = date.today().year + 1
    imported_count = 0

    # The NIH API will only return a max of 500 grants per request, and the default page size is 25 
    # So we request one month at a time, and step through each page
    for year in range(2022, max_year):
        for month in range(12, 13):
            print(f'==================== Imported so far: {imported_count} ==========================')
            print(f'==================== Retrieving month {year}-{month} ======================')

            for offset in range(0, 500, 25):
                grants = retrieve_nih_grants(year, month, offset)                
                if grants is None:
                    break
                print(f"Received {len(grants)} grants")                          
                for g in grants:
                    process_grant(g)
                    # TODO -- remove this when really running
                    return
                imported_count += len(grants)
        
        
def retrieve_nih_grants(year, month, offset):
    if month < 10:
        monthstr = f'0{month}'
    else:
        monthstr = month
    monthfilter = f"&dateStart={monthstr}/01/{year}&dateEnd={monthstr}/31/{year}"

    print("Reading from NIH API")
    criteria = nih_query_criteria(offset)
    
    response = requests.post(url = NIH_BASE,
                             data = json.dumps(criteria),
                             headers={"Content-Type":"application/vnd.api+json"})
    print("-----")
    response_json = response.json()
    grants = response_json['results']
    print(grants[1])
    return grants


def nih_query_criteria(offset):
    c =  {
        "criteria":
        {
            "covid_response": ["Reg-CV", "CV"]
        },
        "include_fields": [
            "ProjectTitle","AbstractText","FiscalYear","Organization", "ProjectNum","OrgCountry",
            "ProjectNumSplit","ContactPiName","PrincipalInvestigators","ProgramOfficers",
            "ProjectStartDate","ProjectEndDate",
            "AwardAmount", "AgencyIcFundings", "PrefTerms",
        ],
        "offset": offset,
        "limit":25
    }
    return c


def process_grant(grant):
    print(f" -- processing grant {grant['project_num']} -- {grant['project_title']}")

    existing_grant = find_cic_grant(grant['project_num'])
    print(f"    -- existing grant is {type(existing_grant)}")
    grant_json = nih_to_cic_format(grant)
    if existing_grant is None:        
        print("   -- not found - creating")
        response_code = create_cic_grant(grant_json)
    else:
        print("   -- found! updating")
        response_code = update_cic_grant(grant_json, existing_grant['id'])
        
    print(f"    -- {response_code}")

    
def find_cic_grant(grant_id):
    # TODO -- this cycles through all grants until it finds the correct ID; should really just request one by ID through the CIC API
    print(f" -- Looking for existing grant {grant_id}")
    response = requests.get(f"{CIC_GRANTS_API}")
    response_json = response.json()    
    cic_grants = response_json['data']
    while(len(cic_grants) > 0):
        for cg in cic_grants:
            if cg['attributes']['award_id'] == grant_id:
                print(f"   -- found {cg['attributes']['award_id']}")
                return cg
        if response_json['links']['next'] is not None:
            print('.', end='', flush=True)
            response = requests.get(f"{response_json['links']['next']}")
            response_json = response.json()    
            cic_grants = response_json['data']
        else:
            print(" -- Expected more grants, but 'next' link is missing")
            cic_grants = []

            
def find_cic_person(first, last):
    # TODO -- this cycles through all people until it finds the correct ID; should really just request one by ID through the CIC API
    print(f" -- Looking for existing person {first} {last}")
    response = requests.get(f"{CIC_PEOPLE_API}")
    response_json = response.json()    
    cic_people = response_json['data']
    while(len(cic_people) > 0):
        for cp in cic_people:
            if cp['attributes']['first_name'] == first and cp['attributes']['last_name'] == last:
                print(f"   -- found person {cp['id']}")
                return cp
        if response_json['links']['next'] is not None:
            print('.', end='', flush=True)
            response = requests.get(f"{response_json['links']['next']}")
            response_json = response.json()    
            cic_people = response_json['data']
        else:
            print(" -- Expected more people, but 'next' link is missing")
            cic_people = []

            
def person_name_to_cic_format(first, last):
    person_data = {
        "data": {
            "type": "Person",
            "attributes": {
                "first_name": first,
                "last_name": last
        }}}
    return person_data

    
def nih_to_cic_format(grant):
    grant_data = {
        "data": {
            "type": "Grant", 
            "attributes": {
                "funder_divisions": nih_funding_divisions(grant['agency_ic_fundings']),
                "keywords": nih_keywords(grant['pref_terms']),
                "program_officials": nih_program_officials(grant['program_officers']),
#                "other_investigators": [ ],
                "principal_investigator": nih_principal_investigator(grant['principal_investigators']),
                "funder": {
                    "type": "Funder",
                    "id": 4 # TODO -- this should be looked up!
                },
#                "awardee_organization": {
#                    "type": "Organization",
#                    "id": 4
#                },
#                "awardee_organization": {
#                    "id": 4,
#                    "ror": "https://ror.org/05dq2gs74",
#                    "name": "Vanderbilt University Medical Center",
#                    "country": "United States"
#                },
                "award_id": grant['project_num'],
                "title": grant['project_title'],
                "start_date": nih_to_cic_date(grant['project_start_date']),
                "end_date": nih_to_cic_date(grant['project_end_date']),
                "award_amount": grant['award_amount'],
                "abstract": grant['abstract_text']
            }
        }
    }
    return grant_data


def nih_principal_investigator(people):
    # Create the appropriate people, then return them as an array of references like
    #  {
    #    "type": "Person",
    #    "id": "1"
    #  }

    first = people[0]['first_name']
    if len(people[0]['middle_name']) > 0:
        first += ' ' + people[0]['middle_name']
    last = people[0]['last_name']

    person = find_or_create_person(first,last)
    person_json = { "type": "Person",
                    "id": int(person['id']) }
    print(f" -- attaching person {person_json}")
    return person_json


def nih_program_officials(grant_officials):
    # Create the appropriate people, then return them as an array of references like
    # [
    #  {
    #    "type": "Person",
    #    "id": "1"
    #  }
    # ]

    first = grant_officials[0]['first_name']
    if len(grant_officials[0]['middle_name']) > 0:
        first += ' ' + grant_officials[0]['middle_name']
    last = grant_officials[0]['last_name']

    person = find_or_create_person(first,last)

    return [ { "type": "Person",
               "id": int(person['id']) } ]


def find_or_create_person(first, last):
    # see if person exists
    person = find_cic_person(first, last)

    if person is None:
        person = create_cic_person(person_name_to_cic_format(first, last))

    return person


def nih_keywords(s):
    if(s is None or len(s) == 0):
        return []
    else:
        # TODO -- return s.split(';')
        return s[0:98] 

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


def create_cic_grant(grant_json):
    r = requests.post(url = CIC_GRANTS_API,
                      data = json.dumps(grant_json),
                      headers={"Content-Type":"application/vnd.api+json"})
    if r.status_code >= 300:
        print(f"ERROR {r} {r.text}")
        
    return r.json()['data']


def create_cic_person(person_json):
    r = requests.post(url = CIC_PEOPLE_API,
                      data = json.dumps(person_json),
                      headers={"Content-Type":"application/vnd.api+json"})
    if r.status_code >= 300:
        print(f"ERROR {r} {r.text}")
    print(f" -- created person {r.json()}")
    return r.json()['data']


def update_cic_grant(grant_json, grant_id):
    grant_json['data']['id'] = grant_id
    print(f" -- updating grant with {grant_json}")
    r = requests.patch(url = CIC_GRANTS_API + f"/{grant_id}",
                      data = json.dumps(grant_json),
                      headers={"Content-Type":"application/vnd.api+json"})
    if r.status_code >= 300:
        print(f"ERROR {r} {r.text}")
    return r
    

if __name__ == "__main__":
    main()
