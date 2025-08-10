from datetime import date, datetime
from pyquery import PyQuery 
import cic_grants
import cic_orgs
import cic_people
import cic_publications
import html_entity_cleaner
import json
import logging
import re
import requests
import time
import urllib.parse

# DOI query
# https://api.crossref.org/v1/works/10.1007%2F978-3-030-15705-0_13

# Note tha CrossRef uses "minimal" DOIs, with 10.xxxx
# CIC uses "full" DOIS, with https://doi.org/10.xxx

CROSSREF_MEMBERS = "https://api.crossref.org/members"
CROSSREF_WORK_BASE = "https://api.crossref.org/v1/works/"

def main():
    #testing
    test_doi = "10.1007/978-3-030-15705-0_13"
    mdoi = cic_publications.minimize_doi(test_doi)
    print(mdoi)
    work = retrieve_crossref_work(mdoi)
    print("======== Retrieved =========")
    print(work)
    print("======== Converted =========")
    new_work = process_work(work)
    print(new_work)
    print("======== Done  =========")

    
def process_work(work):
    # convert to cic format
    new_work = crossref_to_cic_format(work)
    # sent do cic
    return(new_work)

def retrieve_crossref_work(doi):
    print(f"Retrieving work by DOI: {doi}")
    response = requests.get(url = CROSSREF_WORK_BASE + doi,
                            headers={"Content-Type":"application/vnd.api+json"})
    return response.json()['message']

 
def crossref_to_cic_format(pub):
    pub_data = {
        "data": {
            "type": "Publication", 
            "attributes": {
                "keywords": [],
                "title": html_entity_cleaner.replace_quoted(pub['title'][0])
            }
        }
    }
    return pub_data

    
def members_list():
    # https://api.crossref.org/members?offset=0&rows=100
    page_size = 100
    imported_count = 0

    text_file = open("crossref_members.txt", "w")
    
    for offset in range(0,24400, page_size):
        members = get_members(offset, page_size)    
        print(f"Found {len(members)} members, total {imported_count}")
        
        # extract members
        for m in members:
            # print(f"   {m['primary-name']}")
            text_file.write(f"{m['primary-name']}\n")
            
        time.sleep(1)    
        imported_count += len(members)
        
    text_file.close()
    print(f"Total imported: {imported_count}")

    
def get_members(offset, page_size):
    member_url = f"{CROSSREF_MEMBERS}?offset={offset}&rows={page_size}"
    response = requests.get(member_url)
    response_json = response.json()    
    return response_json['message']['items']

    
if __name__ == "__main__":
    main()
