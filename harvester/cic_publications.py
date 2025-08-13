import cic_config
import json
import logging
import requests

CIC_PUBLICATIONS_API = f"{cic_config.CIC_BASE}/v1/publications"
CIC_PUBLICATIONS_SEARCH_API = f"{cic_config.CIC_BASE}/search/publications"

def main():
    print("CIC publications demo")
    print("")
    d = find_cic_publication('https://doi.org/10.1371/journal.pone.0265252')
    print(d)

    
def minimize_doi(doi):
    # if it starts with 10, it's good
    if doi.startswith("10."):
        return doi
    # remove 'doi:'
    if doi.startswith("doi:"):
        return doi[4:]
    # else, return anything that looks like a DOI (e.g., remove the prefix from 'http(s)://xxx.doi.org/10.....')
    match = re.search(r"10.*.", doi)
    return match.group()


def full_doi(doi):
    mdoi = minimize_doi(doi)
    return "https://doi.org/" + mdoi


def create_cic_publication(publication_json):
    r = requests.post(url = CIC_PUBLICATIONS_API,
                      data = json.dumps(publication_json),
                      headers={"Content-Type":"application/vnd.api+json",
                               "Authorization": f"access_token {cic_config.CIC_TOKEN}"
                      })
    if r.status_code >= 300:
        logging.error(f"{r} {r.text}")
        print(f"ERROR {r} {r.text}")
        return {}
    logging.info(f" -- created publication {r.json()}")
    return r.json()['data']


def update_cic_publication(publication_json, publication_id):
    grant_json['data']['id'] = publication_id
    logging.info(f" -- updating publication with {publication_json}")
    r = requests.patch(url = CIC_PUBLICATIONS_API + f"/{publication_id}",
                      data = json.dumps(publication_json),
                      headers={"Content-Type":"application/vnd.api+json",
                               "Authorization": f"access_token {cic_config.CIC_TOKEN}"
                      })
    if r.status_code >= 300:
        logging.error(f"{r} {r.text}")
        print(f"ERROR {r} {r.text}")
    return r


def delete_cic_publication(publication_id):
    logging.info(f" -- deleting publication {publication_id}")

    response = requests.delete(url = CIC_PUBLICATIONS_API + f"/{publication_id}",
                               headers={"Content-Type":"application/vnd.api+json",
                                        "Authorization": f"access_token {cic_config.CIC_TOKEN}"
                               })
    logging.info(f"    -- {response}")
    
    
def find_cic_publication(doi):
    logging.debug(f" -- Looking for existing publication {doi}")
    logging.debug(f"    -- {CIC_PUBLICATIONS_SEARCH_API}?keyword={doi}")
    response = requests.get(f"{CIC_PUBLICATIONS_SEARCH_API}?keyword={doi}")
    response_json = response.json()
    if  'hits' not in response_json:
        return None
    if  'hits' not in response_json['hits']:
        return None
    cic_publications = response_json['hits']['hits']
    for d in cic_publications:        
        logging.debug(f" --  checking {d['_id']} {d['_source']['doi']}")
        if '_source' in d and d['_source']['doi'] == doi:
            return d['_source']
    return None


# Find a page of publications
def find_cic_publications(page = 1):
    logging.debug(" -- Reading publications from CIC API")
    response = requests.get(f"{CIC_PUBLICATIONS_API}?page%5Bnumber%5D={page}")
    response_json = response.json()
    if 'data' not in response_json:
        return []
    publications = response_json['data']
    return publications



if __name__ == "__main__":
    main()
