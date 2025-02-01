import cic_grants
import cic_orgs
import cic_people
import csv
import json
import logging
import requests

################################
# add_radx_studies
#
# Utility to add RADx studies to grants. Cycles through all grants in the system. If the grant is present in the RADx 
# data, the relevant RADx fields are added.
################################

def add_radx_to_grant(radx, grant):
    # compare authors
    print(f" -- {radx[3]} -- {grant['principal_investigator']['first_name']} {grant['principal_investigator']['last_name']}")

#    cic_grants.update_cic_grant(grant_update_json(title, abstract), grant['id'])
    
def grant_update_json(title, abstract):
    grant_data = {
        "data": {
            "type": "Grant", 
            "attributes": {
                "title": title,
                "abstract": abstract
            }
        }
    }
    return grant_data

    
    
def main():
    found = 0
    with open('RADx_2024-12.csv', newline='') as csvfile:
        lines = csv.reader(csvfile, delimiter=',', quotechar='"')
        for line in lines:
            g = cic_grants.find_cic_grant(line[4])
            if g is not None:
                print(f"{line[4]} --> {g['id']}")
                found = found + 1
                add_radx_to_grant(line, g)
    print(f"Found {found} matching grants.")



if __name__ == "__main__":
    main()
