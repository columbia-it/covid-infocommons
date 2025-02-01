import cic_assets
import cic_grants
import cic_orgs
import cic_people
import requests
import json

# NOTE: The exports below are not a "complete" export. They clean data by filtering out:
#       - private email addresses, so we can publish the data in Dryad with a bit of privacy protection
#       - approved flags, since data in CIC is almost always approved, and these are clutter


def main():
    export_people()
        
def export_people():
    with open("cic_people_emails_export.csv", "w") as outfile:
        # process all people, one page at a time
        for page in range(1, 100000):
            people = cic_people.find_cic_people(page)            
            if people is None or len(people) == 0:
                break
            print(f"Page {page} -- {len(people)} people")
            for p in people:
                # Filter private emails for privacy purposes
                if 'private_emails' in ['attributes']:
                    del p['attributes']['private_emails']
                # Remove extra 'approved' attributes
                if 'approved' in p['attributes']:
                    del p['attributes']['approved']
                for af in p['attributes']['affiliations']:
                        if 'approved' in af:
                            del af['approved']

                # Write to CSV
                if p['attributes']['emails'] is not None and len(p['attributes']['emails']) > 0:                    
                    outfile.write(f"{p['attributes']['first_name']} {p['attributes']['last_name']}, {single_value(p['attributes']['emails'])}\n")
        print("Completed people export to \'cic_people_emails_export.csv\'.")
        print("IMPORTANT! This export may contain duplicates. For best results, run it through Unix sort and uniq")

def single_value(s):
    if s.startswith("["):
        first_comma = s.index(",")
        return s[1:first_comma]
    else:
        return s
        
def remove_empty_from_dict(d):
    if type(d) is dict:
        return dict((k, remove_empty_from_dict(v)) for k, v in d.items() if v and remove_empty_from_dict(v))
    elif type(d) is list:
        return [remove_empty_from_dict(v) for v in d if v and remove_empty_from_dict(v)]
    else:
        return d

if __name__ == "__main__":
    main()
