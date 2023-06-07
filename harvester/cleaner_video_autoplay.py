import cic_assets
import json
import logging
import requests

# Updates assets that have the autoplay setting to remove that setting

def main():
    # process all assets, one page at a time
    page = 1
    assets = cic_assets.find_cic_assets(page)
    total = len(assets)
    print(f"Received {len(assets)} assets")
    while assets is not None and len(assets) > 0:
        for a in assets:
            dp = a['attributes']['download_path']
            if 'autoplay=1' in dp:
                print(f"  changeme: {dp}")
                print(f"  {a}")
                asset_id = a['id']
                person_id = a['attributes']['author']['id']
                changed_dp = dp.replace('autoplay=1','autoplay=0')
                print(f"  {id}")
                print(f"  {person_id}")
                print(f"  {changed_dp}")
                new_json = {
                    "data": {
                        "type": "Asset",
                        "attributes": {
                            "filename": 'cic_video',
                            "download_path": changed_dp,
                            "author": {
                                "type": "Person",
                                "id": person_id
                            }
                    }}}
                print(f"  {new_json}")
                cic_assets.update_cic_asset(new_json, asset_id)
        page += 1
        assets = cic_assets.find_cic_assets(page)
        if assets is not None:
            total += len(assets)
            print(f"Received {len(assets)} assets, total {total}")
    print("Completed autoplay cleaning")



if __name__ == "__main__":
    main()
