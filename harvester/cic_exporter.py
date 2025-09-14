import cic_assets
import cic_datasets
import cic_grants
import cic_orgs
import cic_people
import cic_publications
import requests
import json

# NOTE: The exports below are not a "complete" export. They clean data by filtering out:
#       - email addresses, so we can publish the data in Dryad with a bit of privacy protection
#       - approved flags, since data in CIC is almost always approved, and these are clutter


def main():
    export_people()
    export_grants()
    export_orgs()
    export_assets()
    export_datasets()
    export_publications()

def export_assets():
    with open("cic_assets_export.json", "w") as outfile:
        outfile.write("[")
        any_written = False
        # process all assets, one page at a time
        for page in range(1, 100000):
            assets = cic_assets.find_cic_assets(page)
            if assets is None or len(assets) == 0:
                break
            print(f"Page {page} -- {len(assets)} assets")
            for a in assets:
                # Filter emails for privacy purposes
                if 'emails' in a['attributes']['author']:
                    del a['attributes']['author']['emails']
                if 'private_emails' in a['attributes']['author']:
                    del a['attributes']['author']['private_emails']
                # Remove extra 'approved' attributes
                if 'approved' in a['attributes']:
                    del a['attributes']['approved']
                if 'approved' in a['attributes']['author']:
                    del a['attributes']['author']['approved']
                json_object = json.dumps(remove_empty_from_dict(a), indent=4)
                if any_written:
                    outfile.write(",")
                outfile.write(json_object)
                any_written = True

        outfile.write("]")
        print("Completed asset export to \'cic_assets_export.json\'")

    
def export_grants():
    with open("cic_grants_export.json", "w") as outfile:
        outfile.write("[")
        any_written = False
        # process all grants, one page at a time
        for page in range(1, 100000):
            grants = cic_grants.find_cic_grants(page)
            if grants is None or len(grants) == 0:
                break
            print(f"Page {page} -- {len(grants)} grants")
            for g in grants:
                # Filter emails for privacy purposes
                if g['attributes']['principal_investigator'] is not None and 'emails' in g['attributes']['principal_investigator']:
                    del g['attributes']['principal_investigator']['emails']
                if g['attributes']['principal_investigator'] is not None and 'private_emails' in g['attributes']['principal_investigator']:
                    del g['attributes']['principal_investigator']['private_emails']
                # Remove extra 'approved' attributes
                if 'approved' in g['attributes']:
                    del g['attributes']['approved']
                if g['attributes']['funder'] is not None and 'approved' in g['attributes']['funder']:
                    del g['attributes']['funder']['approved']
                if g['attributes']['principal_investigator'] is not None and 'approved' in g['attributes']['principal_investigator']:
                    del g['attributes']['principal_investigator']['approved']
                if g['attributes']['awardee_organization'] is not None and 'approved' in g['attributes']['awardee_organization']:
                    del g['attributes']['awardee_organization']['approved']
                for po in g['attributes']['program_officials']:
                    if 'approved' in po:
                        del po['approved']
                for oi in g['attributes']['other_investigators']:
                    if 'approved' in oi:
                        del oi['approved']
                if g['attributes']['principal_investigator'] is not None:
                    for af in g['attributes']['principal_investigator']['affiliations']:
                        if 'approved' in af:
                            del af['approved']
                    
                json_object = json.dumps(remove_empty_from_dict(g), indent=4)
                if any_written:
                    outfile.write(",")
                outfile.write(json_object)
                any_written = True

        outfile.write("]")
        print("Completed grant export to \'cic_grants_export.json\'")

        
def export_orgs():
    with open("cic_orgs_export.json", "w") as outfile:
        outfile.write("[")
        any_written = False
        # process all orgs, one page at a time
        for page in range(1, 100000):
            orgs = cic_orgs.find_cic_orgs(page)
            if orgs is None or len(orgs) == 0:
                break
            print(f"Page {page} -- {len(orgs)} orgs")            
            for o in orgs:
                # Remove extra 'approved' attributes
                if 'approved' in o['attributes']:
                    del o['attributes']['approved']

                json_object = json.dumps(remove_empty_from_dict(o), indent=4)
                if any_written:
                    outfile.write(",")
                outfile.write(json_object)
                any_written = True

        outfile.write("]")
        print("Completed orgs export to \'cic_orgs_export.json\'")


def export_datasets():
    with open("cic_datasets_export.json", "w") as outfile:
        outfile.write("[")
        any_written = False
        # process all datasets, one page at a time
        for page in range(1, 100000):
            dats = cic_datasets.find_cic_datasets(page)
            if dats is None or len(dats) == 0:
                break
            print(f"Page {page} -- {len(dats)} datasets")            
            for d in dats:
                # Remove extra 'approved' attributes
                if 'approved' in d['attributes']:
                    del d['attributes']['approved']

                json_object = json.dumps(remove_empty_from_dict(d), indent=4)
                if any_written:
                    outfile.write(",")
                outfile.write(json_object)
                any_written = True

        outfile.write("]")
        print("Completed datasets export to \'cic_datasets_export.json\'")


def export_publications():
    with open("cic_publications_export.json", "w") as outfile:
        outfile.write("[")
        any_written = False
        # process all publications, one page at a time
        for page in range(1, 100000):
            pubs = cic_publications.find_cic_publications(page)
            if pubs is None or len(pubs) == 0:
                break
            print(f"Page {page} -- {len(pubs)} publications")            
            for p in pubs:
                # Remove extra 'approved' attributes
                if 'approved' in p['attributes']:
                    del p['attributes']['approved']

                json_object = json.dumps(remove_empty_from_dict(p), indent=4)
                if any_written:
                    outfile.write(",")
                outfile.write(json_object)
                any_written = True

        outfile.write("]")
        print("Completed publications export to \'cic_publications_export.json\'")

        
def export_people():
    with open("cic_people_export.json", "w") as outfile:
        outfile.write("[")
        any_written = False
        # process all people, one page at a time
        for page in range(1, 100000):
            people = cic_people.find_cic_people(page)
            if people is None or len(people) == 0:
                break
            print(f"Page {page} -- {len(people)} people")
            for p in people:
                # Filter emails for privacy purposes
                if 'emails' in p['attributes']:
                    del p['attributes']['emails']
                if 'private_emails' in ['attributes']:
                    del p['attributes']['private_emails']
                # Remove extra 'approved' attributes
                if 'approved' in p['attributes']:
                    del p['attributes']['approved']
                for af in p['attributes']['affiliations']:
                        if 'approved' in af:
                            del af['approved']
                
                json_object = json.dumps(remove_empty_from_dict(p), indent=4)
                if any_written:
                    outfile.write(",")
                outfile.write(json_object)
                any_written = True

        outfile.write("]")
        print("Completed people export to \'cic_people_export.json\'")

def remove_empty_from_dict(d):
    if type(d) is dict:
        return dict((k, remove_empty_from_dict(v)) for k, v in d.items() if v and remove_empty_from_dict(v))
    elif type(d) is list:
        return [remove_empty_from_dict(v) for v in d if v and remove_empty_from_dict(v)]
    else:
        return d

if __name__ == "__main__":
    main()
