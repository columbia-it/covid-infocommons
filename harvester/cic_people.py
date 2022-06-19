import cic_config
import json
import logging
import requests

CIC_PEOPLE_API = f"{cic_config.CIC_BASE}/v1/people"


def main():
    print("CIC people demo")
    print()
    print(f"Find in CIC: {find_cic_person('Shreeram','Akilesh')}")

    
def find_or_create_person(first, last, email = '', link = ''):
    # see if person exists
    person = find_cic_person(first, last)

    if not email:
        email = ''
    if person is None:
        person = create_cic_person(person_name_to_cic_format(first, last, email, link))

    return person
                  
def create_cic_person(person_json):
    r = requests.post(url = CIC_PEOPLE_API,
                      data = json.dumps(person_json),
                      headers={"Content-Type":"application/vnd.api+json",
                               "Authorization": f"access_token {cic_config.CIC_TOKEN}"
                      })
    if r.status_code >= 300:
        print(f"ERROR {r} {r.text}")
        logging.error(f"{r} {r.text}")
        return None
    logging.info(f" -- created person {r.json()}")
    return r.json()['data']


def person_name_to_cic_format(first, last, email = '', link = ''):
    person_data = {
        "data": {
            "type": "Person",
            "attributes": {
                "first_name": first,
                "last_name": last,
                "emails": email,
                "private_emails": link
        }}}
    return person_data


# Find the first page of people
def find_cic_people():
    logging.debug(" -- Reading people from CIC API")
    response = requests.get(CIC_PEOPLE_API)
    response_json = response.json()
    people = response_json['data']
    return people


def find_cic_person(first, last):
    logging.debug(f" -- Looking for existing person {first} {last}")
    response = requests.get(f"{CIC_PEOPLE_API}?filter[last_name={last}")
    response_json = response.json()
    if response.status_code >= 300 or 'data' not in response_json:
        return None
    cic_people = response_json['data']
    while(len(cic_people) > 0):
        for cp in cic_people:
            if cp['attributes']['first_name'] == first and cp['attributes']['last_name'] == last:
                logging.debug(f"   -- found person {cp['id']}")
                return cp
        if response_json['links']['next'] is not None:
            print('.', end='', flush=True)
            response = requests.get(f"{response_json['links']['next']}")
            response_json = response.json()    
            cic_people = response_json['data']
        else:
            cic_people = []


def delete_cic_person(person_id):
    logging.info(f" -- deleting person {person_id}")

    r = requests.delete(url = CIC_PEOPLE_API + f"/{person_id}",
                               headers={"Content-Type":"application/vnd.api+json",
                                        "Authorization": f"access_token {cic_config.CIC_TOKEN}"
                               })
    if r.status_code >= 300:
        print(f"ERROR {r} {r.text}")
        logging.error(f"{r} {r.text}")
            

if __name__ == "__main__":
    main()
