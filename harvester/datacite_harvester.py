from datetime import date, datetime
from pyquery import PyQuery 
import cic_grants
import cic_orgs
import cic_people
import html_entity_cleaner
import json
import logging
import requests
import time


DATACITE_BASE = "https://api.datacite.org/dois?query=covid+OR+COVID+OR+covid19+OR+coronavirus+OR+pandemic+OR+sars2+OR+SARS-CoV"

def main():
    # https://api.test.datacite.org/dois?query=covid&page[number]=2&page[size]=100
    page_size = 100
    imported_count = 0

    for page in range(1,3): #100000):
        datasets = get_datasets(page, page_size)
        if datasets is None or len(datasets) == 0:
            break
        print(f"Found {len(datasets)} datasets, total {imported_count}")
        
        for d in datasets:
            print(f"   {d['id']} {d['attributes']['titles'][0]['title']}")
            
            process_dataset(d)
        imported_count += len(datasets)
        time.sleep(2)
        
    print(f"Total imported: {imported_count}")


def process_dataset(d):
    existing_data = cic_datasets.find_cic_dataset(d['id'])
    response_code = ''
    if existing_data is None:
        # No pre-existing dataset, so we're creating one from scratch
        logging.debug("   -- not found - creating")
        #grant_json = nsf_to_cic_format(grant)
        #response_code = cic_grants.create_cic_grant(grant_json)

        logging.info(f"    -- {response_code}")


    
def get_datasets(page, page_size):
    datasets_url = f"{DATACITE_BASE}&page[number]={page}&page[size]={page_size}"
    print(f"Searching {datasets_url}")
    response = requests.get(datasets_url)
    response_json = response.json()
    print(f"TOTAL RESPONSE: {response_json['meta']['total']}")
    return response_json['data']

    
if __name__ == "__main__":
    main()
