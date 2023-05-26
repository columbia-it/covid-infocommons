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


CROSSREF_MEMBERS = "https://api.crossref.org/members"

def main():
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
