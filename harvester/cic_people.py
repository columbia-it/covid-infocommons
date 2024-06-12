import cic_config
import cic_orgs
import json
import logging
import requests

CIC_PEOPLE_API = f"{cic_config.CIC_BASE}/v1/people"


def main():
    print("CIC people demo")
    print()
    person = find_cic_person('Shreeram','Akilesh')
    print(f"Find in CIC: {person}")

    
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


def update_cic_person(person_json, person_id):
    person_json['data']['id'] = person_id
    logging.info(f" -- updating person {person_id} with {person_json}")
    r = requests.patch(url = CIC_PEOPLE_API + f"/{person_id}",
                      data = json.dumps(person_json),
                      headers={"Content-Type":"application/vnd.api+json",
                               "Authorization": f"access_token {cic_config.CIC_TOKEN}"
                      })
    if r.status_code >= 300:
        logging.error(f"{r} {r.text}")
        print(f"ERROR {r} {r.text}")
    return r


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


def person_org_to_cic_format(person, org_id):
    person_data = {
        "data": {
            "type": "Person", 
            "attributes": {
                "first_name": person['first_name'],
                "last_name": person['last_name'],
                "emails": person['emails'],
                "private_emails": person['private_emails'],
                "affiliations": [
                    {
                        "type": "Organization",
                        "id": org_id
                    }
                ]
            }
        }
    }
    return person_data


# Find the first page of people
def find_cic_people(page = 1):
    logging.debug(" -- Reading people from CIC API")
    response = requests.get(f"{CIC_PEOPLE_API}?page%5Bnumber%5D={page}")
    response_json = response.json()
    if response_json is None or 'data' not in response_json:
        return None
    people = response_json['data']
    return people


def find_cic_person(first, last):
    first = first.strip()
    last = last.strip()
    logging.debug(f" -- Looking for existing person {first} {last}")
    response = requests.get(f"{CIC_PEOPLE_API}?filter[last_name]={last}")
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
            if response_json is not None and 'data' in response_json:
                cic_people = response_json['data']
            else:
                cic_people = []
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


def backup_to_json():
    print("exporting for backup")
    with open("cic_people.json", "w") as outfile:
        outfile.write("[")

        # process all people, one page at a time
        for page in range(1, 100000):
            people = find_cic_people(page)
            if people is None or len(people) == 0:
                break
            print(f"Page {page} -- {len(people)} people")
            for p in people:
                json_object = json.dumps(p, indent=4)
                outfile.write(json_object)
                outfile.write(",")

        outfile.write("]")
        print("Completed export to \'cic_people.json\'")


if __name__ == "__main__":
    main()
    
