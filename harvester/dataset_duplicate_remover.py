import cic_datasets
import cic_config
import json
import logging
import re
import requests
import urllib.parse

################################
# dataset_duplicate_remover
#
# Utility to identify duplicate datasets and remove them.
#
################################

CIC_DATASETS_SEARCH_API = f"{cic_config.CIC_BASE}/search/datasets"

# process
# Takes a dataset(d) and boolean(delete_dups)
#
# Searches for duplicates of the dataset. If delete_dups is True, any duplicates are removed, but not
# the original dataset itself.
#
# Returns True if the datset OR a duplicate is found in the system, and False if the dataset does not
# yet exist in the system.
def process(d, did, delete_dups):
    print(f"Processing {d['doi']} -- {did}")

    # Find datasets with similar titles
    enc_title = url_encode(d['title'])
    #print(f"searching {CIC_DATASETS_SEARCH_API}?keyword=\"{enc_title}\"")
    response = requests.get(f"{CIC_DATASETS_SEARCH_API}?keyword=\"{enc_title}\"")
    response_json = response.json()
    if  'hits' not in response_json:
        return False
    if  'hits' not in response_json['hits']:
        return False
    possible_dups = response_json['hits']['hits']

    match_found = False
    
    # For each, if the title is exactly the same, AND the authors are exactly the same
    # Delete it
    for pd in possible_dups:
        if (str(pd['_source']['id']) == str(did)):
            # we found the request dataset; don't consider it to be a dupe of itself
            match_found = True
        elif pd['_source']['title'] == d['title']:
            print(f"POSSIBLE DUPE! {pd['_source']['id']} -- {pd['_source']['title']}")

            # Since the titles match, assume it is a matc until we find out otherwise
            match_found = True
            for i in range(0,len(pd['_source']['authors'])):
                ap = pd['_source']['authors'][i]
                ad = d['authors'][i]
                if (ap['first_name'] != ad['first_name']) or (ap['last_name'] != ad['last_name']):
                    # If the names don't match, we want to move to the next dataset without saying match_found
                    match_found = False
                    print("  -- NOT MATCH -- ")
            
            if match_found and delete_dups:
                # TODO: if it's still a match, delete it
                print(f"  -- TO DELETE {pd['_source']['id']} is a dupe of {did}")
                cic_datasets.delete_cic_dataset(pd['_source']['id'])

    return match_found


def url_encode(s):
    safe_string = urllib.parse.quote_plus(s)
    return safe_string


def main():
    # process all datasets, one page at a time
    page = 1
    total = 0
    dd = cic_datasets.find_cic_datasets()
    print(f"Received {len(dd)} datasets")
    while len(dd) > 0:
        total += len(dd)
        for d in dd:
            process(d['attributes'], d['id'], True)
        page += 1

        dd = cic_datasets.find_cic_datasets(page)
        print(f"Received {len(dd)} datasets -- total {total}")
    print("Completed dataset processing")


if __name__ == "__main__":
    main()
    
