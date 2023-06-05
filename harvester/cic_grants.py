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
#    grant = find_cic_grant('3R43CA243815-01S2')
#    if grant is None:
    grant = find_cic_grant('2204082')
    print(f" -- found {grant['id']} -- {grant['award_id']} -- {grant['title']}")
#    grant_json = grant_object_to_upload_json(grant)
#    update_cic_grant(grant_json, grant['id'])
#    delete_cic_grant(10721)


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
    
    
def find_cic_grant(award_id):
    logging.debug(f" -- Looking for existing grant {award_id}")
    logging.debug(f"    -- {CIC_GRANTS_SEARCH_API}?keyword={award_id}")
    response = requests.get(f"{CIC_GRANTS_SEARCH_API}?keyword={award_id}")
    response_json = response.json()
    if  'hits' not in response_json:
        return None
    if  'hits' not in response_json['hits']:
        return None
    cic_grants = response_json['hits']['hits']
    for cg in cic_grants:
        logging.debug(f" --  checking {cg['_id']}")
        if cg['_source']['award_id'] == award_id:
            logging.debug(f"   -- found {cg['_source']['award_id']}")
            # copy the id into the internal metadata, so it has the same structure as the rest of the API
            cg['_source']['id'] = cg['_id']
            return cg['_source']
    return None

def grant_object_to_upload_json(grant):
    # converts from the CIC output format to the CIC upload format
    print(f"Converting to upload JSON -- {grant}")
    grant_data = {
        "data": {
            "type": "Grant", 
            "attributes": {
                "funder": {
                    "type": "Funder",
                    "id": grant['funder']['id']
                },
                "funder_divisions": grant['funder_divisions'],
                "program_reference_codes": grant['program_reference_codes'],
                "program_officials": person_array_to_reference_array(grant['program_officials']),                
                "other_investigators": person_array_to_reference_array(grant['other_investigators']),                
                "principal_investigator": person_to_reference(grant['principal_investigator']),                
                "awardee_organization": org_to_reference(grant['awardee_organization']),
                "keywords": grant['keywords'],                
                "award_id": grant['id'],
                "title": grant['title'],
                "start_date": grant['start_date'],
                "end_date": grant['end_date'],
                "award_amount": grant['award_amount'],
                "abstract": grant['abstract'],
                "approved": grant['approved']
            }
        }
    }
    print(f"upload JSON is -- {grant_data}")
    return grant_data


def person_array_to_reference_array(people):
    ref_array = []
    for p in people:
        ref_array.append(person_to_reference(p))
    return ref_array

def person_to_reference(person):
    reference = { "type": "Person",
                  "id": person['id']
    }
    return reference

def org_to_reference(org):
    reference = { "type": "Organization",
                  "id": org['id']
    }
    return reference

# Find a page of grants
def find_cic_grants(page = 1):
    logging.debug(" -- Reading grants from CIC API")
    response = requests.get(f"{CIC_GRANTS_API}?page%5Bnumber%5D={page}")
    response_json = response.json()
    if 'data' not in response_json:
        return []
    grants = response_json['data']
    return grants



if __name__ == "__main__":
    main()
