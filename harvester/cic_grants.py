import cic_config
import json
import requests

CIC_GRANTS_API = f"{cic_config.CIC_BASE}/v1/grants"
CIC_GRANTS_SEARCH_API = f"{cic_config.CIC_BASE}/search/grants"

def main():
    print("CIC grant demo")
    print("")
    print("finding test grant 2030139")
    grant = find_cic_grant('2030139')
    print(f" -- found {grant['id']} -- {grant['award_id']} -- {grant['title']}")


def create_cic_grant(grant_json):
    r = requests.post(url = CIC_GRANTS_API,
                      data = json.dumps(grant_json),
                      headers={"Content-Type":"application/vnd.api+json"})
    if r.status_code >= 300:
        print(f"ERROR {r} {r.text}")
        
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


def find_cic_grant(grant_id):
    print(f" -- Looking for existing grant {grant_id}")
    response = requests.get(f"{CIC_GRANTS_SEARCH_API}?award_id={grant_id}")
    response_json = response.json()
    cic_grants = response_json['hits']['hits']
    for cg in cic_grants:
        print(f" --  checking {cg}")
        if cg['_source']['award_id'] == grant_id:
            print(f"   -- found {cg['_source']['award_id']}")
            # copy the id into the internal metadata, so it has the same structure as the rest of the API
            cg['_source']['id'] = cg['_id']
            return cg['_source']
    return None
            

if __name__ == "__main__":
    main()
