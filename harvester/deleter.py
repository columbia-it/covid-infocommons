import cic_grants
import cic_orgs
import cic_people
import json
import logging
import requests
    
def main():
    # process all grants, one page at a time
    grants = cic_grants.find_cic_grants()
    print(f"Received {len(grants)} grants")
    while len(grants) > 0:
        for g in grants:
            cic_grants.delete_cic_grant(g['id'])
        grants = cic_grants.find_cic_grants()
        print(f"Received {len(grants)} grants")
    print("Completed grant deletion")

    # process all people, one page at a time
    people = cic_people.find_cic_people()
    print(f"Received {len(people)} people")
    while len(people) > 0:
        for p in people:
            cic_people.delete_cic_person(p['id'])
        people = cic_people.find_cic_people()
        print(f"Received {len(people)} people")
    print("Completed people deletion")

    # process all orgs, one page at a time
    orgs = cic_orgs.find_cic_orgs()
    print(f"Received {len(orgs)} orgs")
    while len(orgs) > 0:
        for o in orgs:
            cic_orgs.delete_cic_org(o['id'])
        orgs = cic_orgs.find_cic_orgs()
        print(f"Received {len(orgs)} orgs")
    print("Completed org deletion")



if __name__ == "__main__":
    main()
