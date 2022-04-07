
import requests, json


def main():
    grants = retrieve_grants()
    print(f"Received {len(grants)} grants")
    for g in grants:
        handle_grant(g)    
        

def retrieve_grants():
    NSF_GRANT_REQUEST = "https://api.nsf.gov/services/v1/awards.json?keyword=covid+covid-19+corid-19+corvid-19+coronavirus+sars2+%22SARS-CoV-2%22&printFields=abstractText,agency,awardAgencyCode,awardee,awardeeAddress,awardeeCity,awardeeCountryCode,awardeeCounty,awardeeDistrictCode,awardeeName,awardeeStateCode,awardeeZipCode,cfdaNumber,coPDPI,date,dunsNumber,estimatedTotalAmt,expDate,fundAgencyCode,fundProgramName,fundsObligatedAmt,id,offset,parentDunsNumber,pdPIName,perfAddress,perfCity,perfCountryCode,perfCounty,perfDistrictCode,perfLocation,perfStateCode,perfZipCode,piEmail,piFirstName,piLastName,piMiddeInitial,piPhone,poEmail,poName,poPhone,primaryProgram,projectOutComesReport,publicationConference,publicationResearch,rpp,startDate,title,transType&offset=0"

    print("Reading from NSF API")
    print(f"REQUEST = {NSF_GRANT_REQUEST}")

    response = requests.get(NSF_GRANT_REQUEST)
    print("-----")
    response_json = response.json()
    print(type(response_json))
    grants = response_json['response']['award']
    return grants


def handle_grant(grant):
    print(f" -- processing grant {grant['title']}")
    grant_json = cic_json_format(grant)
    response_code = deposit_grant(grant_json)
    print(f"    -- {response_code}")


def cic_json_format(grant):
    grant_data = {
        "data": {
            "type": "Grant", 
            "attributes": {
                "funder_divisions": ["research", "department"],
                "program_reference_codes": ["CK090", "RND123"],
                "keywords": ["covid", "research"],
                "program_officials": [
                    {
                        "type": "Person",
                        "id": "1"
                    }
                ],
                "other_investigators": [ ],
                "principal_investigator": {
                    "type": "Person",
                    "id": "1"
                },
                "funder": {
                    "type": "Funder",
                    "id": 1
                },
                "awardee_organization": {
                    "type": "Organization",
                    "id": 2
                },
                "award_id": grant['id'],
                "title": grant['title'],
                "start_date": "2020-01-01",
                "end_date": "2022-12-31",
                "award_amount": grant['estimatedTotalAmt'],
                "abstract": grant['abstractText']
            }
        }
    }
    return grant_data
    

def deposit_grant(grant_json):
    API_ENDPOINT = "https://cice-prod.paas.cc.columbia.edu/v1/grants"    
    r = requests.post(url = API_ENDPOINT,
                      data = json.dumps(grant_json),
                      headers={"Content-Type":"application/vnd.api+json"})
    return r
    
    
print("The value of __name__ is:", repr(__name__))
if __name__ == "__main__":
    main()
