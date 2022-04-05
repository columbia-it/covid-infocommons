
import requests, json


def main():
    print("Reading from NSF API")

    NSF_GRANT_REQUEST = "https://api.nsf.gov/services/v1/awards.json?keyword=covid+covid-19+corid-19+corvid-19+coronavirus+sars2+%22SARS-CoV-2%22&printFields=abstractText,agency,awardAgencyCode,awardee,awardeeAddress,awardeeCity,awardeeCountryCode,awardeeCounty,awardeeDistrictCode,awardeeName,awardeeStateCode,awardeeZipCode,cfdaNumber,coPDPI,date,dunsNumber,estimatedTotalAmt,expDate,fundAgencyCode,fundProgramName,fundsObligatedAmt,id,offset,parentDunsNumber,pdPIName,perfAddress,perfCity,perfCountryCode,perfCounty,perfDistrictCode,perfLocation,perfStateCode,perfZipCode,piEmail,piFirstName,piLastName,piMiddeInitial,piPhone,poEmail,poName,poPhone,primaryProgram,projectOutComesReport,publicationConference,publicationResearch,rpp,startDate,title,transType&offset=0"

    print(f"REQUEST = {NSF_GRANT_REQUEST}")

    # Read content from a URL and parse as JSON
    response = requests.get(NSF_GRANT_REQUEST)
    response_text = response.text
    response_parse = json.loads(response_text)    
    print(type(response_parse))
    grants = response_parse['response']['award']    
    print(f"Received {len(grants)} grants")

    for g in grants:
        handle_grant(g)
        


def handle_grant(grant):
    print(f" -- grant {grant['title']}")
    
    # TODO: Send the grant to our API
    
print("The value of __name__ is:", repr(__name__))
if __name__ == "__main__":
    main()
