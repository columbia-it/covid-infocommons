from datetime import date, datetime
from pyquery import PyQuery
import cic_datasets
import cic_grants
import cic_orgs
import cic_people
import html_entity_cleaner
import json
import logging
import requests
import time


START_PAGE = 1
DATACITE_BASE = "https://api.datacite.org/dois?query=covid+OR+COVID+OR+covid19+OR+coronavirus+OR+pandemic+OR+sars2+OR+SARS-CoV"
DATACITE_TEST = "https://api.datacite.org/dois?query=scherle"

ALLOWED_FUNDERS = [
    'National Science Foundation', 'NSF',
    'National Institutes of Health', 'NIH',
    'Agency for Healthcare Research and Quality', 'Agency for Healthcare Research and Quality (AHRQ)',
    'National Cancer Institute', 'National Cancer Institute (NCI)',
    'National Eye Institute', 'National Eye Institute (NEI)',
    'National Heart Lung and Blood Institute', 'National Heart Lung and Blood Institute (NHLBI)',
    'National Human Genome Research Institute', 'National Human Genome Research Institute (NHGRI)',
    'National Institute on Aging', 'National Institute on Aging (NIA)',
    'National Institute on Alcohol Abuse and Alcoholism', 'National Institute on Alcohol Abuse and Alcoholism (NIAAA)',
    'National Institute of Allergy and Infectious Diseases', 'National Institute of Allergy and Infectious Diseases (NIAID)',
    'National Institute of Arthritis and Musculoskeletal and Skin Diseases', 'National Institute of Arthritis and Musculoskeletal and Skin Diseases (NIAMS)',
    'National Institute of Arthritits and Musculoskeletal and Skin Diseases', 'National Institute of Arthritis and Musculoskeletal and Skin Diseases (NIAMS)',
    'National Institute of Biomedical Imaging and Bioengineering', 'National Institute of Biomedical Imaging and Bioengineering (NIBIB)',
    'Eunice Kennedy Shriver National Institute of Child Health and Human Development', 'Eunice Kennedy Shriver National Institute of Child Health and Human Development (NICHD)',
    'National Institute on Deafness and Other Communication Disorders', 'National Institute on Deafness and Other Communication Disorders (NIDCD)',
    'National Institute of Dental and Craniofacial Research', 'National Institute of Dental and Craniofacial Research (NIDCR)',
    'National Institute of Diabetes and Digestive and Kidney Diseases', 'National Institute of Diabetes and Digestive and Kidney Diseases (NIDDK)',
    'National Institute on Drug Abuse', 'National Institute on Drug Abuse (NIDA)',
    'National Institute of Environmental Health Sciences', 'National Institute of Environmental Health Sciences (NIEHS)',
    'National Institute of General Medical Sciences', 'National Institute of General Medical Sciences (NIGMS)',
    'National Institute of Mental Health', 'National Institute of Mental Health (NIMH)',
    'National Institute on Minority Health and Health Disparities', 'National Institute on Minority Health and Health Disparities (NIMHD)',
    'National Institute of Neurological Disorders and Stroke', 'National Institute of Neurological Disorders and Stroke (NINDS)',
    'National Institute of Nursing Research', 'National Institute of Nursing Research (NINR)',
    'National Library of Medicine', 'National Library of Medicine (NLM)',
    'NIH Clinical Center', 'NIH Clinical Center (CC)',
    'Center for Information Technology', 'Center for Information Technology (CIT)',
    'Center for Scientific Review', 'Center for Scientific Review (CSR)',
    'Fogarty International Center', 'Fogarty International Center (FIC)',
    'John E. Fogarty International Center for Advanced Study in the Health Sciences', 'Fogarty International Center (FIC)',
    'National Center for Advancing Translational Sciences', 'National Center for Advancing Translational Sciences (NCATS)',
    'National Center for Complementary and Integrative Health', 'National Center for Complementary and Integrative Health (NCCIH)',
    'National Center for Complementary and Intergrative Health', 'National Center for Complementary and Integrative Health (NCCIH)',
    'National Center for Emerging and Zoonotic Infectious Diseases', 'National Center for Emerging and Zoonotic Infectious Diseases (NCEZID)',
    'National Institute for Occupational Safety and Health', 'National Institute for Occupational Safety and Health (NIOSH)',
    'National Center for Immunization and Respiratory Diseases', 'National Center for Immunization and Respiratory Diseases (NCIRD)',
    'National Center for Injury Prevention and Control', 'National Center for Injury Prevention and Control (NCIPC)',
    'NIH Office of the Director', 'NIH Office of the Director'

    ]

def main():
    # https://api.test.datacite.org/dois?query=covid&page[number]=2&page[size]=100
    page_size = 100
    imported_count = 0

    for page in range(START_PAGE, 100000):
        datasets = get_datasets(page, page_size)
        if datasets is None or len(datasets) == 0:
            break
        print(f"Found {len(datasets)} datasets, total {imported_count}")

        for d in datasets:            
            process_dataset(d)

        imported_count += len(datasets)
        time.sleep(2)

    print(f"Total imported: {imported_count}")


def process_dataset(d):
    print(f"------------------ {d['id']} -----------")
    print(f"   {d['id']} {d['attributes']['titles'][0]['title']}")

    # only process datasets associated with an NSF or NIH grant
    print(f"   {d['attributes']['fundingReferences']}")
    funders = d['attributes']['fundingReferences']
    funder_found = False
    if funders is None or len(funders) == 0:
        return None
    for f in funders:
        if f['funderName'] in ALLOWED_FUNDERS:
            funder_found = True
            break
        else:
            print(f"  UNKOWN FUNDER {f['funderName']}")
    if not funder_found:
        return None           

    
    # don't overwrite an existing dataset
    existing_data = cic_datasets.find_cic_dataset(d['id'])
    print(f"   found pre-existing? {existing_data != None}")
    response_code = ''
    if existing_data is None:
        # No pre-existing dataset, so we're creating one from scratch
        # Transform to CIC format and save
        print("   -- not found - creating")
        dataset_json = datacite_to_cic_format(d)
        print(f"  NEW DATASET {dataset_json}")
        response_code = cic_datasets.create_cic_dataset(dataset_json)
        print(f"    -- response {response_code}")
        


def datacite_to_cic_format(d):
    da = d['attributes']
    dataset_data = {
        "data": {
            "type": "Dataset", 
            "attributes": {
                "doi": d['id'],
                "title": html_entity_cleaner.replace_quoted(da['titles'][0]['title']),
                "downloadPath": "https://doi.org/" + d['id'],
                "size": datacite_size(da),
                "authors": process_datacite_authors(da),
                "grants": process_datacite_funding(da)
            }
        }
    }
    return dataset_data


def datacite_size(da):
    if da['sizes'] is None or len(da['sizes']) == 0:
        return ""
    else:
        return da['sizes'][0]

def process_datacite_funding(da):
    print(f" FUNDING {da['fundingReferences']}")
    results = []
    # Find the appropriate grant objects, then return them as an array of references like
    #  {
    #    "type": "Grant",
    #    "id": "1"
    #  }
    if 'fundingReferences' not in da:
        return None
    dc_grants = da['fundingReferences']
    for g in dc_grants:
        if 'awardNumber' not in g:
            continue
        award = g['awardNumber']
        grant = cic_grants.find_cic_grant(award)
        if grant is None:
            continue
        grant_json = { "type": "Grant",
                    "id": int(grant['id']) }
        print(f" -- attaching grant {grant_json}")
        results.append(grant_json)
    print(f" -- results {results}")
    return results


def process_datacite_authors(da):
    print(f" AUTHOr {da['creators']}")
    results = []
    # Create the appropriate people, then return them as an array of references like
    #  {
    #    "type": "Person",
    #    "id": "1"
    #  }
    if 'creators' not in da:
        return None
    people = da['creators']
    for p in people:
        first = ''
        if 'givenName' in p:
            first = p['givenName']
        last = ''
        if 'familyName' in p:
            last = p['familyName']
        orcid = find_orcid(p['nameIdentifiers'])
        affiliation = find_affiliation(p['affiliation'])
        person = cic_people.find_or_create_person(first, last, '', '', orcid, affiliation)
        if person is None:
            continue
        person_json = { "type": "Person",
                    "id": int(person['id']) }
        print(f" -- attaching person {person_json}")
        results.append(person_json)
    print(f" -- results {results}")
    return results

def find_affiliation(afs):
    if len(afs) > 0:
        return afs[0]
    else:
        return afs
        

def find_orcid(ids):
    for i in ids:
        if i['nameIdentifierScheme'] != 'ORCID':
            continue
        if i['nameIdentifier'].startswith("https://orcid.org/"):
            return i['nameIdentifier'][len("https://orcid.org/"):]
        else:
            return i['nameIdentifier']
    return None
    

def get_datasets(page, page_size):
    datasets_url = f"{DATACITE_BASE}&page[number]={page}&page[size]={page_size}"
    #datasets_url = f"{DATACITE_TEST}&page[number]={page}&page[size]={page_size}"
    print(f"Searching {datasets_url}")
    response = requests.get(datasets_url)
    response_json = response.json()
    print(f"TOTAL RESPONSE: {response_json['meta']['total']}")
    return response_json['data']

    
if __name__ == "__main__":
    main()
