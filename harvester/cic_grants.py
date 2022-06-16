import cic_config
import json
import logging
import requests

CIC_GRANTS_API = f"{cic_config.CIC_BASE}/v1/grants"
CIC_GRANTS_SEARCH_API = f"{cic_config.CIC_BASE}/search/grants"

def main():
    print("CIC grant demo")
    print("")
    print("finding test grant 3R43CA243815-01S2")
    grant = find_cic_grant('3R43CA243815-01S2')
    print(f" -- found {grant['id']} -- {grant['award_id']} -- {grant['title']}")


def create_cic_grant(grant_json):
    r = requests.post(url = CIC_GRANTS_API,
                      data = json.dumps(grant_json),
                      headers={"Content-Type":"application/vnd.api+json",
                               "Authorization": f"access_token {cic_config.CIC_TOKEN}"
                      })
    if r.status_code >= 300:
        logging.error(f"{r} {r.text}")
        print(f"ERROR {r} {r.text}")
        return {}
    logging.info(f" -- created grant {r.json()}")
    return r.json()['data']


def update_cic_grant(grant_json, grant_id):
    grant_json['data']['id'] = grant_id
    logging.info(f" -- updating grant with {grant_json}")
    r = requests.patch(url = CIC_GRANTS_API + f"/{grant_id}",
                      data = json.dumps(grant_json),
                      headers={"Content-Type":"application/vnd.api+json",
                               "Authorization": f"access_token {cic_config.CIC_TOKEN}"
                      })
    if r.status_code >= 300:
        logging.error(f"{r} {r.text}")
        print(f"ERROR {r} {r.text}")
    return r


def delete_cic_grant(grant_id):
    logging.info(f" -- deleting grant {grant_id}")

    response = requests.delete(url = CIC_GRANTS_API + f"/{grant_id}",
                               headers={"Content-Type":"application/vnd.api+json",
                                        "Authorization": f"access_token {cic_config.CIC_TOKEN}"
                               })
    logging.info(f"    -- {response}")
    
    
def find_cic_grant(grant_id):
    logging.debug(f" -- Looking for existing grant {grant_id}")
    logging.debug(f"    -- {CIC_GRANTS_SEARCH_API}?keyword={grant_id}")
    response = requests.get(f"{CIC_GRANTS_SEARCH_API}?keyword={grant_id}")
    response_json = response.json()
    cic_grants = response_json['hits']['hits']
    for cg in cic_grants:
        logging.debug(f" --  checking {cg['_id']}")
        if cg['_source']['award_id'] == grant_id:
            logging.debug(f"   -- found {cg['_source']['award_id']}")
            # copy the id into the internal metadata, so it has the same structure as the rest of the API
            cg['_source']['id'] = cg['_id']
            return cg['_source']
    return None


# Find a page of grants
def find_cic_grants(page = 1):
    logging.debug(" -- Reading grants from CIC API")
    response = requests.get(f"{CIC_GRANTS_API}?page%5Bnumber%5D={page}")
    response_json = response.json()
    grants = response_json['data']
    return grants



if __name__ == "__main__":
    main()
