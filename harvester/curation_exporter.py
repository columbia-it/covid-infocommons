
import csv
import requests
import json

# export URLs like
# https://cice-dev.paas.cc.columbia.edu/admin/apis/grant/60/change/

CIC_BASE = "https://cic-apps-dev.datascience.columbia.edu/"
CIC_GRANT_REQUEST = f"{CIC_BASE}/v1/grants"
    
def main():
    with open('grant_curation.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['ID', 'AwardNumber', 'Title', 'EditLink'])
        # process all grants, one page at a time
        for page in range(1, 1000000):
            grants = retrieve_cic_grants(page)
            if grants is None:
                break
            print(f"Received {len(grants)} grants")
            for g in grants:
                csv_writer.writerow([g['id'], g['attributes']['award_id'], g['attributes']['title'], f"{CIC_BASE}/admin/apis/grant/{g['id']}/change/"])
        print("Completed grant export to \'grant_curation.csv\'")
        

def retrieve_cic_grants(page):
    request_url = f"{CIC_GRANT_REQUEST}?page%5Bnumber%5D={page}"
    print("Reading grants from CIC API")
    print(f"REQUEST = {request_url}")

    response = requests.get(request_url)
    if response.status_code >= 400:
        return
    print("-----")
    response_json = response.json()
    grants = response_json['data']
    return grants


if __name__ == "__main__":
    main()

