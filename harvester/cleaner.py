
import requests, json

CIC_BASE = "https://cice-dev.paas.cc.columbia.edu"
CIC_GRANT_REQUEST = f"{CIC_BASE}/v1/grants"
    
def main():
    # process all grants, one page at a time
    grants = retrieve_cic_grants()
    print(f"Received {len(grants)} grants")
    while len(grants) > 0:
        for g in grants:
            delete_grant(g)
        grants = retrieve_cic_grants()
        print(f"Received {len(grants)} grants")
    print("Completed grant deletion")
        

def retrieve_cic_grants():

    print("Reading grants from CIC API")
    print(f"REQUEST = {CIC_GRANT_REQUEST}")

    response = requests.get(CIC_GRANT_REQUEST)
    print("-----")
    response_json = response.json()
    grants = response_json['data']
    return grants


def delete_grant(grant):
    print(f" -- processing grant {grant['id']} -- {grant['attributes']['title']}")

    response = requests.delete(f"{CIC_GRANT_REQUEST}/{grant['id']}")
    print(f"    -- {response}")
    
    

if __name__ == "__main__":
    main()
