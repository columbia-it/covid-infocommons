import cic_grants
import cic_people
import cic_orgs
import requests
import json
    
def main():
    import_orgs()
    import_people()
    import_grants()

    
def import_grants():
    return None


def import_orgs():
    # read from the export file
    with open('cic_orgs_export.json') as f:
        orgs = json.load(f)
        print(f'Found {len(orgs)} orgs')

    # for each item found, import it
    index = 1
    for o in orgs:
        print(index)
        o_result = cic_orgs.find_or_create_org( o['attributes']['name'],
                                                o['attributes']['country'],
                                                o['attributes']['state'],
        )
        print(f"got {o_result}")
        index += 1
        
    return None


def import_people():
    return None


if __name__ == "__main__":
    main()


