import cic_grants
import cic_orgs
import cic_people
import json
import logging
import requests

def process(grant):
    print(f"Processing {grant['award_id']}")
    org = grant['awardee_organization']
    print(f" -- {org['id']}")
    pi = grant['principal_investigator']
    print(f" -- {pi['emails']} {pi['first_name']} {pi['last_name']}")

    person = cic_people.find_cic_person(pi['first_name'], pi['last_name'])
    print(f" -- person {person}")
    person_affil = person['attributes']['affiliations']
    print(f" -- af {person_affil}")
    if person_affil is None or len(person_affil) == 0:
        print(" -- replacing affiliation")
        person_json = cic_people.person_org_to_cic_format(person['attributes'], org['id'])
        print(f"person_json {person_json}")
        cic_people.update_cic_person(person_json, person['id'])
        
        

    
def main():
    # process all grants, one page at a time
    grants = cic_grants.find_cic_grants()
    print(f"Received {len(grants)} grants")
    page = 1
    while len(grants) > 0:
        for g in grants:
            process(g['attributes'])
        grants = cic_grants.find_cic_grants(page)
        print(f"Received {len(grants)} grants")
        page += 1
    print("Completed grant processing")


if __name__ == "__main__":
    main()
