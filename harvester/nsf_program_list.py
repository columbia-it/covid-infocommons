import cic_grants
import cic_orgs
import cic_people
import json
import logging
import requests
import nsf_harvester

# Checks the database for values in a specific field

def main():
    # process all grants, one page at a time
    page = 1
    grants = cic_grants.find_cic_grants(page)
    print(f"Received {len(grants)} grants")
    while len(grants) > 0:
        for g in grants:
           if 'funder_divisions' in g['attributes']:
                val = g['attributes']['funder_divisions'][0]
                if val not in nsf_harvester.DIVISION_TO_DIRECTORATE:
                    print(f"{g['attributes']['award_id']} -- {val}")
        page += 1
        grants = cic_grants.find_cic_grants(page)
        print(f"Received {len(grants)} grants")
    print("Completed grant deletion")

if __name__ == "__main__":
    main()
