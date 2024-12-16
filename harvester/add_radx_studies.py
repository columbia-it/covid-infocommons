import cic_grants
import cic_orgs
import cic_people
import json
import logging
import requests

################################
# add_radx_studies
#
# Utility to add RADx studies to grants. Cycles through all grants in the system. If the grant is present in the RADx 
# data, the relevant RADx fields are added.
################################

def process(grant):
    if grant['funder']['id'] != 4:
        return
    print(f"Processing {grant['award_id']} -- ")
    org = grant['awardee_organization']
    pi = grant['principal_investigator']
    #if pi is None or org is None:
    #    return
    #person = cic_people.find_cic_person(pi['first_name'], pi['last_name'])
    #if person is None or person['attributes'] is None:
    #    return
    #person_affil = person['attributes']['affiliations']
    #if person_affil is None or len(person_affil) == 0:
    #    print(" -- replacing affiliation")
    #    person_json = cic_people.person_org_to_cic_format(person['attributes'], org['id'])
    #    cic_people.update_cic_person(person_json, person['id'])

    
def main():
    # process all grants, one page at a time
    grants = cic_grants.find_cic_grants()
    print(f"Received {len(grants)} grants")
    page = 1
    total = 0
    while len(grants) > 0:
        total += len(grants)
        for g in grants:
            process(g['attributes'])
        grants = cic_grants.find_cic_grants(page)
        print(f"Received {len(grants)} grants -- total {total}")
        page += 1
    print("Completed grant processing")


if __name__ == "__main__":
    main()
