import cic_config
import json
import requests

CIC_ORGS_API = f"{cic_config.CIC_BASE}/v1/organizations"
ROR_API = "https://api.ror.org/organizations"


def main():
    print("CIC org demo")
    print()
    print(f"Find in CIC: {find_cic_org('Education Cities')}")
    print(f"Find in ROR: {find_ror_org('Duke University')}")
    print(f"Find in ROR: {find_ror_org('Duke UniVERsity')}")
    print(f"find_or_create: {find_or_create_org('CROW Canyon Archaeological Center', 'United States')}")
    
    
def find_cic_org(name):
    # TODO --- update to use search instead of cycling through all
    print(f" -- find {name} from {CIC_ORGS_API}")
    response = requests.get(f"{CIC_ORGS_API}")
    response_json = response.json()    
    cic_orgs = response_json['data']
    while(len(cic_orgs) > 0):
        for co in cic_orgs:
            if co['attributes']['name'] == name:
                print(f"   -- found {co['attributes']['name']}")
                return co
        if response_json['links']['next'] is not None:
            print('.', end='', flush=True)
            response = requests.get(f"{response_json['links']['next']}")
            response_json = response.json()    
            cic_orgs = response_json['data']
        else:
            return None


def find_cic_org_by_ror(ror_id):
    # TODO --- update to use filtering instead of cycling through all
    print(f" -- find {ror_id} from {CIC_ORGS_API}")
    response = requests.get(f"{CIC_ORGS_API}")
    response_json = response.json()    
    cic_orgs = response_json['data']
    while(len(cic_orgs) > 0):
        for co in cic_orgs:
            if co['attributes']['ror'] == ror_id:
                print(f"   -- found {co['attributes']['ror']}")
                return co
        if response_json['links']['next'] is not None:
            print('.', end='', flush=True)
            response = requests.get(f"{response_json['links']['next']}")
            response_json = response.json()    
            cic_orgs = response_json['data']
        else:
            return None

        
def find_ror_org(name, country = 'United States'):
    name = name.lower()
    country = country.lower()
    print(f" -- find {name} from {ROR_API}")
    response = requests.get(f"{ROR_API}?query={name}")
    response_json = response.json()
    print(f" -- found {response_json['number_of_results']} results")
    if response_json['number_of_results'] == 0:
        return None
    else:
        # check the name and country of each
        # return first exact match (case insensitive)
        for ro in response_json['items']:
            if ro['name'].lower() == name and ro['country']['country_name'].lower() == country:
                print(f"   -- found {ro['name']}")
                return ro

    
def find_or_create_org(name, country):
    org = find_cic_org(name)
    if org is None:
        ror_org = find_ror_org(name, country)        
        if ror_org is not None:
            org = find_cic_org_by_ror(ror_org['id'])
            if org is None:
                org = create_cic_org(org_to_cic_format(ror_org['name'], country, ror_org['id']))
        else:
            org = create_cic_org(org_to_cic_format(name, country, None))
    return org       


def create_cic_org(org_json):
    r = requests.post(url = CIC_ORGS_API,
                      data = json.dumps(org_json),
                      headers={"Content-Type":"application/vnd.api+json",
                               "Authorization": f"access_token {cic_config.CIC_TOKEN}"
                      })
    if r.status_code >= 300:
        print(f"ERROR {r} {r.text}")
        
    return r.json()['data']


def org_to_cic_format(name, country, ror = None):
    org_data = {
        "data": {
            "type": "Organization",
            "attributes": {
                "name": name,
                "country": country
        }}}
    if ror is not None:
        org_data['data']['attributes']['ror'] = ror
    return org_data
            

if __name__ == "__main__":
    main()
