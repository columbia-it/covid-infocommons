import cic_grants
import cic_orgs
import cic_people
import json
import logging
import requests

################################
# pi_migrate_from_drupal
#
# Utility to enhance PI entries by scraping the Drupal web pages
################################

def process(person):
    #print(f"Processing {person}")
    meta = person['attributes']
    if meta is None:
        return
    if meta['private_emails'] is not None and len(meta['private_emails']) > 0:
        print(f"email {meta['private_emails']}")

     
    
def main():    
    # process all people, one page at a time
    people = cic_people.find_cic_people()
    print(f"Received {len(people)} people")
    page = 1
    total = 0
    while len(people) > 0:
        total += len(people)
        for p in people:
            #print(f"Processing {p['id']}")
            process(p)
        people = cic_people.find_cic_people(page)
        print(f"Received {len(people)} people -- total {total}")
        page += 1
    print("Completed PI processing")


if __name__ == "__main__":
    main()

