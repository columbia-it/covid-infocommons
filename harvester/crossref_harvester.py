from datetime import date, datetime
from pyquery import PyQuery 
import cic_grants
import cic_orgs
import cic_people
import html_entity_cleaner
import json
import logging
import re
import requests
import time


# DOI query
# https://api.crossref.org/v1/works/10.1007%2F978-3-030-15705-0_13

CROSSREF_MEMBERS = "https://api.crossref.org/members"
CROSSREF_WORK_BASE = "https://api.crossref.org/v1/works/"

def main():
    #testing
    test_doi = "10.1007%2F978-3-030-15705-0_13"
    doi = normalize_doi(test_doi)
    print(doi)
    work = retrieve_crossref_work(doi)
    print(work)

def normalize_doi(doi):
    # if it starts with 10, it's good
    if doi.startswith("10."):
        return doi
    # remove 'doi:'
    if doi.startswith("doi:"):
        return doi[4:]
    # else, return anything that looks like a DOI (e.g., remove the prefix from 'http(s)://xxx.doi.org/10.....')
    match = re.search(r"10.*.", doi)
    return match.group()
    
def retrieve_crossref_work(doi):
    print(f"Retrieving work by DOI: {doi}")
    response = requests.get(url = CROSSREF_WORK_BASE + doi,
                            headers={"Content-Type":"application/vnd.api+json"})
    return response.json()

    
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
