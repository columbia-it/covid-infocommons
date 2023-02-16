import cic_config
import cic_people
import json
import logging
import requests

CIC_ASSETS_API = f"{cic_config.CIC_BASE}/v1/assets"


def main():
    print("CIC assets demo")
    print()
    assets = find_assets_for_person(573)
    print(f"For person 573:")
    for a in assets:
        print(f" -- asset {a['id']}")
    print("----")
    person = cic_people.find_cic_person('Florence D','Hudson')
    print(f"Found Florence in CIC with id {person['id']}")
    assets = find_assets_for_person(int(person['id']))
    print(f"Florence's assets:")
    for a in assets:
        print(f" -- asset {a['id']}")
    print("----")
    asset = find_or_create_for_person('florence_placeholder', 'https://example.com/florence_placeholder_asset', 3099)
    print(f"Placeholder asset {asset}")


def find_assets_for_person(id):
    found = []
    page = 1
    assets = find_cic_assets(page)
    while assets is not None:
        for a in assets:
            aa = a['attributes']
            if 'author' in aa and aa['author']['id'] == id:
                found.append(a)
        page += 1
        assets = find_cic_assets(page)
    return found


def find_or_create_for_person(filename, download_path, pi_id):
    assets = find_assets_for_person(pi_id)
    for a in assets:
        if a['attributes']['filename'] == filename:
            return a
    a = create_cic_asset(filename, download_path, pi_id)
    return a


def find_cic_assets(page = 1):
    logging.debug(f" -- Reading assets from CIC API page={page}")
    response = requests.get(f"{CIC_ASSETS_API}?page%5Bnumber%5D={page}")
    response_json = response.json()
    if 'data' not in response_json:
        return None
    assets = response_json['data']
    return assets


def create_cic_asset(filename, download_path, pi_id):
    asset_json = {
        "data": {
            "type": "Asset",
            "attributes": {
                "filename": filename,
                "download_path": download_path,
                "author": {
                        "type": "Person",
                        "id": pi_id
                }
    }}}
    r = requests.post(url = CIC_ASSETS_API,
                      data = json.dumps(asset_json),
                      headers={"Content-Type":"application/vnd.api+json",
                               "Authorization": f"access_token {cic_config.CIC_TOKEN}"
                      })
    if r.status_code >= 300:
        print(f"ERROR {r} {r.text}")
        logging.error(f"{r} {r.text}")
        return None
    logging.info(f" -- created asset {r.json()}")
    return r.json()['data']


if __name__ == "__main__":
    main()
    
