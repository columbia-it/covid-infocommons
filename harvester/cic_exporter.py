import cic_assets
import cic_grants
import cic_orgs
import cic_people
import requests
import json
    
def main():
#    export_grants()
#    export_people()
#    export_orgs()
    export_assets()

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
                json_object = json.dumps(a, indent=4)
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
                json_object = json.dumps(g, indent=4)
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
                json_object = json.dumps(o, indent=4)
                if any_written:
                    outfile.write(",")
                outfile.write(json_object)
                any_written = True

        outfile.write("]")
        print("Completed orgs export to \'cic_orgs_export.json\'")

        
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
                json_object = json.dumps(p, indent=4)
                if any_written:
                    outfile.write(",")
                outfile.write(json_object)
                any_written = True

        outfile.write("]")
        print("Completed people export to \'cic_people_export.json\'")


if __name__ == "__main__":
    main()
