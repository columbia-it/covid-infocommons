from datetime import date, datetime
import requests, json

CIC_BASE = "https://cice-dev.paas.cc.columbia.edu"
CIC_GRANTS_API = f"{CIC_BASE}/v1/grants"
CIC_FUNDER_API = f"{CIC_BASE}/v1/funders"

NSF_GRANT_REQUEST = "https://api.nsf.gov/services/v1/awards.json?keyword=covid+covid-19+corid-19+corvid-19+coronavirus+sars2+%22SARS-CoV-2%22&printFields=abstractText,agency,awardAgencyCode,awardee,awardeeAddress,awardeeCity,awardeeCountryCode,awardeeCounty,awardeeDistrictCode,awardeeName,awardeeStateCode,awardeeZipCode,cfdaNumber,coPDPI,date,dunsNumber,estimatedTotalAmt,expDate,fundAgencyCode,fundProgramName,fundsObligatedAmt,id,offset,parentDunsNumber,pdPIName,perfAddress,perfCity,perfCountryCode,perfCounty,perfDistrictCode,perfLocation,perfStateCode,perfZipCode,piEmail,piFirstName,piLastName,piMiddeInitial,piPhone,poEmail,poName,poPhone,primaryProgram,projectOutComesReport,publicationConference,publicationResearch,rpp,startDate,title,transType"


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

    print("Reading from NSF API")
    print(f"REQUEST = {nsf_url}")

    response = requests.get(nsf_url)
    print("-----")
    response_json = response.json()    
    grants = response_json['response']['award']
    return grants


def process_grant(grant):
    print(f" -- processing grant {grant['id']} -- {grant['title']}")

    # TODO -- existing_grant = find_cic_grant(grant['id'])
    #         print(f"    -- existing grant is {type(existing_grant)}")
    grant_json = nsf_to_cic_format(grant)
    if 1==1: # TODO -- existing_grant is None:        
        print("   -- not found - creating")
        response_code = deposit_cic_grant(grant_json)
    else:
        print("   -- found! updating")
        response_code = update_cic_grant(grant_json, grant['id'])

        
    print(f"    -- {response_code}")

    
def find_cic_grant(grant_id):
    # TODO -- this cycles through all grants until it finds the correct ID; should really just request one by ID through the CIC API
    print(f" -- Looking for existing grant {grant_id}")
    response = requests.get(f"{CIC_GRANTS_API}")
    response_json = response.json()
    cic_grants = response_json['data']
    for cg in cic_grants:
        print(f"   -- {cg['attributes']['award_id']}")
        if cg['attributes']['award_id'] == grant_id:
            return cg
    print(" -- grant not found")
        

def nsf_to_cic_format(grant):
    grant_data = {
        "data": {
            "type": "Grant", 
            "attributes": {
#                "funder_divisions": [ grant['fundProgramName'] ],
                "program_reference_codes": [],
                "keywords": [],
#                "program_officials": [
#                    {
#                        "type": "Person",
#                        "id": "1"
#                    }
#                ],
                "other_investigators": [ ],
#                "principal_investigator": {
#                    "type": "Person",
#                    "id": "1"
#                },
                "funder": {
                    "type": "Funder",
                    "id": 3 # TODO -- this should be looked up!
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
                "award_id": grant['id'],
                "title": grant['title'],
                "start_date": nsf_to_cic_date(grant['startDate']),
                "end_date": nsf_to_cic_date(grant['expDate']),
                "award_amount": grant['estimatedTotalAmt'],
                "abstract": grant['abstractText']
            }
        }
    }
    return grant_data
    

def nsf_to_cic_date(d):
    parsed = datetime.strptime(d, "%m/%d/%Y")
    iso = parsed.strftime("%Y-%m-%d")
    return iso


def deposit_cic_grant(grant_json):
    r = requests.post(url = CIC_GRANTS_API,
                      data = json.dumps(grant_json),
                      headers={"Content-Type":"application/vnd.api+json"})
    if r.status_code >= 300:
        print(f"ERROR {r} {r.text}")
    return r


def update_cic_grant(grant_json, grant_id):
    r = requests.patch(url = CIC_GRANTS_API + f"/{grant_id}",
                      data = json.dumps(grant_json),
                      headers={"Content-Type":"application/vnd.api+json"})
    if r.status_code >= 300:
        print(f"ERROR {r} {r.text}")
    return r
    

if __name__ == "__main__":
    main()
