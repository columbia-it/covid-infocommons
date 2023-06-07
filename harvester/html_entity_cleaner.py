import cic_grants
import json
import logging
import re
import requests

################################
# html_entity_cleaner
#
# Utility to clean HTML entities and similar tags from grants. Cycles through all
# grants in the system. If the grant title or abstract contains an HTML entity,
# replace it with the equivalent string.
#
################################

def process(grant):
    print(f"Processing {grant['attributes']['award_id']} -- {grant['id']}")


    # if the title or abstract contains a quote, replace it
    changed = False
    p = re.compile('.*[%&].*;')
    title = grant['attributes']['title']
    if title is not None:
        m = p.match(title)
        if m is not None:
            print(f" - title {title}")
            title = replace_quoted(title)
            changed = True
            print(f" - changed to {title}")

    abstract = grant['attributes']['abstract']
    if abstract is not None:
        m = p.match(abstract)
        if m is not None:
            abstract = replace_quoted(abstract)
            changed = True
            print(" - abstract changed")

#    if not changed:
        return

    print(" - running update")
    cic_grants.update_cic_grant(grant_update_json(title, abstract), grant['id'])
    

def replace_quoted(s):
    if s is None:
        return s
    
    s = s.replace("&amp;", "&")
    s = s.replace("&amp", "&")
    s = s.replace("%amp;", "&")
    s = s.replace("%amp", "&")
    s = s.replace("&apos;", "'")
    s = s.replace("&apos", "'")
    s = s.replace("%apos;", "'")
    s = s.replace("%apos", "'")
    s = s.replace("&#039;", "'")
    s = s.replace("&quot;", "\"")
    return s


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
    grant = cic_grants.find_cic_grant('1955260')
    process(grant)
    return

    
    # process all grants, one page at a time
    page = 1
    total = 0
    grants = cic_grants.find_cic_grants()
    print(f"Received {len(grants)} grants")
    while len(grants) > 0:
        total += len(grants)
        for g in grants:
            process(g)
        page += 1
        grants = cic_grants.find_cic_grants(page)
        print(f"Received {len(grants)} grants -- total {total}")
    print("Completed grant processing")


if __name__ == "__main__":
    main()
