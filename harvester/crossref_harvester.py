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
    test_doi = "10.1212/WNL.0000000000010116"
    mdoi = cic_publications.minimize_doi(test_doi)
    print(mdoi)
    work = retrieve_crossref_work(mdoi)
    print("======== Retrieved =========")
    print(work)
    process_work(work, mdoi)
    print("======== Done  =========")

    
def process_work(work, mdoi):
    # send to cic, but don't overwrite an existing publication
    existing_pub = cic_publications.find_cic_publication("https://doi.org/" + mdoi)
    print(f"   found pre-existing? {existing_pub != None}")
    response_code = ''
    if existing_pub is None:
        # No pre-existing publication, so we're creating one from scratch
        # Transform to CIC format and save
        print("   -- not found - creating")
        pub_json = crossref_to_cic_format(work)        
        print(f"  NEW PUBLICATION {pub_json}")
        response_code = cic_publications.create_cic_publication(pub_json)
        print(f"    -- response {response_code}")


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
                "doi": "https://doi.org/" + pub['DOI'],
                "authors": process_crossref_authors(pub),
                "title": html_entity_cleaner.replace_quoted(pub['title'][0])                
            }
        }
    }
    return pub_data


def process_crossref_authors(pub):
    print(f" AUTHOr {pub['author']}")
    results = []

    if 'author' not in pub:
        return None
    people = pub['author']
    for p in people:
        first = ''
        if 'given' in p:
            first = p['given']
        last = ''
        if 'family' in p:
            last = p['family']
        affiliation = find_affiliation(p['affiliation'])
        orcid = find_orcid(p)
        person = cic_people.find_or_create_person(first, last, '', '', orcid, affiliation)
        if person is None:
            continue
        person_json = { "type": "Person",
                    "id": int(person['id']) }
        print(f" -- attaching person {person_json}")
        results.append(person_json)
    print(f" -- results {results}")
    return results


def find_orcid(p):
    if 'ORCID' not in p:
        return None
    return p['ORCID']

def find_affiliation(afs):
    if len(afs) > 0:
        return afs[0]
    else:
        return afs

    
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
