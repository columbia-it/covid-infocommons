import cic_grants
import json
import requests
    
def main():
    # process all grants, one page at a time
    grants = cic_grants.find_cic_grants()
    print(f"Received {len(grants)} grants")
    while len(grants) > 0:
        for g in grants:
            cic_grants.delete_cic_grant(g['id'])
        grants = cic_grants.find_cic_grants()
        print(f"Received {len(grants)} grants")
    print("Completed grant deletion")
        


if __name__ == "__main__":
    main()
