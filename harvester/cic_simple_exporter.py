# A simple exporter that allows us to update our email lists

import cic_assets
import cic_grants
import cic_orgs
import cic_people
import requests
import csv
    
def main():
    export_simple_grants()

    
def export_simple_grants():
    with open("cic_simple_grants_export.csv", "w", newline='') as csvfile:
        csvwriter = csv.writer(csvfile)

        csvwriter.writerow( [
            'principal_investigator.first_name',
	    'principal_investigator.last_name',
	    'principal_investigator.emails',
	    'awardee_organization.name',
	    'funder.name',
	    'award_id',
	    'principal_investigator.id',
	    'principal_investigator.orcid',
	    'id',
	    'title'
        ])
        
        # process all grants, one page at a time
        for page in range(1, 100000):
            grants = cic_grants.find_cic_grants(page)
            if grants is None or len(grants) == 0:
                break
            print(f"Page {page} -- {len(grants)} grants")
            for g in grants:
                ga = g['attributes']

                if ga['awardee_organization'] is not None:
                    awardee_name = ga['awardee_organization']['name']
                if ga['principal_investigator'] is None:
                    continue
                if ga['funder'] is None:
                    continue

                fields = [
                    ga['principal_investigator']['first_name'],
	            ga['principal_investigator']['last_name'],
	            ga['principal_investigator']['emails'],
	            awardee_name,
	            ga['funder']['name'],
	            ga['award_id'],
	            ga['principal_investigator']['id'],
	            ga['principal_investigator']['orcid'],
	            g['id'],
                    ga['title']
                ]
                csvwriter.writerow(fields) 

        print("Completed grant export to \'cic_simple_grants_export.csv\'")


if __name__ == "__main__":
    main()
