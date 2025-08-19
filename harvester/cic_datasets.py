import cic_config
import json
import logging
import requests

CIC_DATASETS_API = f"{cic_config.CIC_BASE}/v1/datasets"
CIC_DATASETS_SEARCH_API = f"{cic_config.CIC_BASE}/search/datasets"

def main():
    print("CIC datasets demo")
    print("")
    d = find_cic_dataset('10.60773/8e0v-pk44')
    print(d)

    # https://cic-apps-dev.datascience.columbia.edu/search/datasets?keyword=https://cic-apps-dev.datascience.columbia.edu/
    d = find_cic_dataset('https://doi.org/10.1016/j.wace.2013.08.002')
    print(d)
    #print(f" -- found {d['id']} --- {d['doi']} --  {d['title']}")
 

def create_cic_dataset(dataset_json):
    r = requests.post(url = CIC_DATASETS_API,
                      data = json.dumps(dataset_json),
                      headers={"Content-Type":"application/vnd.api+json",
                               "Authorization": f"access_token {cic_config.CIC_TOKEN}"
                      })
    if r.status_code >= 300:
        logging.error(f"{r} {r.text}")
        print(f"ERROR {r} {r.text}")
        return {}
    logging.info(f" -- created dataset {r.json()}")
    return r.json()['data']


def update_cic_dataset(dataset_json, dataset_id):
    dataset_json['data']['id'] = dataset_id
    logging.info(f" -- updating dataset with {dataset_json}")
    r = requests.patch(url = CIC_DATASETS_API + f"/{dataset_id}",
                      data = json.dumps(dataset_json),
                      headers={"Content-Type":"application/vnd.api+json",
                               "Authorization": f"access_token {cic_config.CIC_TOKEN}"
                      })
    if r.status_code >= 300:
        logging.error(f"{r} {r.text}")
        print(f"ERROR {r} {r.text}")
    return r


def delete_cic_dataset(dataset_id):
    logging.info(f" -- deleting dataset {dataset_id}")

    response = requests.delete(url = CIC_DATASETS_API + f"/{dataset_id}",
                               headers={"Content-Type":"application/vnd.api+json",
                                        "Authorization": f"access_token {cic_config.CIC_TOKEN}"
                               })
    logging.info(f"    -- {response}")
    
    
def find_cic_dataset(doi):
    logging.debug(f" -- Looking for existing dataset {doi}")
    logging.debug(f"    -- {CIC_DATASETS_SEARCH_API}?keyword={doi}")
    response = requests.get(f"{CIC_DATASETS_SEARCH_API}?keyword={doi}")
    response_json = response.json()
    if  'hits' not in response_json:
        return None
    if  'hits' not in response_json['hits']:
        return None
    cic_datasets = response_json['hits']['hits']
    for d in cic_datasets:        
        logging.debug(f" --  checking {d['_id']} {d['_source']['doi']}")
        if '_source' in d and d['_source']['doi'] == doi:
            return d['_source']
    return None


# Find a page of datasets
def find_cic_datasets(page = 1):
    logging.debug(" -- Reading datasets from CIC API")
    response = requests.get(f"{CIC_DATASETS_API}?page%5Bnumber%5D={page}")
    response_json = response.json()
    if 'data' not in response_json:
        return []
    datasets = response_json['data']
    return datasets



if __name__ == "__main__":
    main()
