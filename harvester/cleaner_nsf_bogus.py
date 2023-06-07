import cic_grants
import cic_orgs
import cic_people
import json
import logging
import requests

# Removes grants that were imported by too-permissive harvesting settings

def main():
    # process all grants, one page at a time
    page = 1
    grants = cic_grants.find_cic_grants(page)
    total = len(grants)
    print(f"Received {len(grants)} grants")
    while len(grants) > 0:
        for g in grants:
            title = g['attributes']['title'].lower()
            if 'abstract' in g['attributes'] and g['attributes']['abstract'] is not None:
                abstract = g['attributes']['abstract'].lower()
            else:
                abstract = ''
            if 'covid' in title or 'sars' in title or 'coronavirus' in title or 'mers' in title or \
               'disease' in title or 'pandemic' in title or 'recovery' in title or 'epidem' in title or 'mask' in title or\
               'immun' in title or 'vaccine' in title or 'ncov' in title or 'virus' in title or \
               'covid' in abstract or 'sars' in abstract or 'coronavirus' in abstract or 'mers' in abstract or \
               'disease' in abstract or 'pandemic' in abstract or 'recovery' in abstract or 'epidem' in abstract or 'mask' in abstract or \
               'immun' in abstract or 'vaccine' in abstract or 'ncov' in abstract or 'virus' in abstract:
                # it's a good grant, do nothing
                1
            else:
                print(f"{g['id']} -- {g['attributes']['title']}")
                cic_grants.delete_cic_grant(g['id'])
        page += 1
        grants = cic_grants.find_cic_grants(page)
        total += len(grants)
        print(f"Received {len(grants)} grants, total {total}")
    print("Completed grant deletion")



if __name__ == "__main__":
    main()
