import cic_config
import json
import requests

CIC_PEOPLE_API = f"{cic_config.CIC_BASE}/v1/people"


def main():
    print("CIC people demo")
    print()
    print(f"Find in CIC: {find_cic_person('Randy','Crichton')}")


def find_or_create_person(first, last):
    # see if person exists
    person = find_cic_person(first, last)

    if person is None:
        person = create_cic_person(person_name_to_cic_format(first, last))

    return person
                  
def create_cic_person(person_json):
    r = requests.post(url = CIC_PEOPLE_API,
                      data = json.dumps(person_json),
                      headers={"Content-Type":"application/vnd.api+json"})
    if r.status_code >= 300:
        print(f"ERROR {r} {r.text}")
    print(f" -- created person {r.json()}")
    return r.json()['data']


def person_name_to_cic_format(first, last):
    person_data = {
        "data": {
            "type": "Person",
            "attributes": {
                "first_name": first,
                "last_name": last
        }}}
    return person_data


def find_cic_person(first, last):
    # TODO -- this cycles through all people until it finds the correct ID; should really just request one by ID through the CIC API
    print(f" -- Looking for existing person {first} {last}")
    response = requests.get(f"{CIC_PEOPLE_API}")
    response_json = response.json()    
    cic_people = response_json['data']
    while(len(cic_people) > 0):
        for cp in cic_people:
            if cp['attributes']['first_name'] == first and cp['attributes']['last_name'] == last:
                print(f"   -- found person {cp['id']}")
                return cp
        if response_json['links']['next'] is not None:
            print('.', end='', flush=True)
            response = requests.get(f"{response_json['links']['next']}")
            response_json = response.json()    
            cic_people = response_json['data']
        else:
            print(" -- Expected more people, but 'next' link is missing")
            cic_people = []



if __name__ == "__main__":
    main()
