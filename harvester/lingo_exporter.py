import cic_grants
import requests
import json
    
def main():
    with open("cic_grants.json", "w") as outfile:
        outfile.write("[")

        # process all grants, one page at a time
        for page in range(1, 100000):
            grants = cic_grants.find_cic_grants(page)
            if grants is None or len(grants) == 0:
                break
            print(f"Page {page} -- {len(grants)} grants")
            for g in grants:
                json_object = json.dumps(grant_to_lingo(g), indent=4)
                outfile.write(json_object)
                outfile.write(",")

        outfile.write("]")
        print("Completed grant export to \'cic_grants.json\'")

def grant_to_lingo(grant):
    g = grant['attributes']
    result = {
        "award_id": g['award_id'],
        "title": g['title'],        
        "funder": grant_funder(g),
        "funder_divisions": g['funder_divisions'],
        "program_official": grant_official(g),
        "start_date": g['start_date'],
        "end_date": g['end_date'],
        "award_amount": g['award_amount'],
        "principal_investigator": grant_pi(g),
        "awardee_organization": grant_org(g),
        "state": grant_state(g),
        "abstract": g['abstract'],
        "keywords": g['keywords']
    }
    return result

def grant_funder(g):
    if g['funder'] is None:
        return ""
    else:
        return g['funder']['name']

    
def grant_pi(g):
    if g['principal_investigator'] is None:
        return ""
    else:
        return g['principal_investigator']['first_name'] + ' ' + g['principal_investigator']['last_name']

    
def grant_official(g):
    if len(g['program_officials']) == 0:
        return ""
    else:
        return g['program_officials'][0]['first_name'] + ' ' + g['program_officials'][0]['last_name']

    
def grant_org(g):
    if g['awardee_organization'] is None:
        return ""
    else:
        return g['awardee_organization']['name']

def grant_state(g):
    if g['awardee_organization'] is None:
        return ""
    else:
        return g['awardee_organization']['state']
    

if __name__ == "__main__":
    main()
