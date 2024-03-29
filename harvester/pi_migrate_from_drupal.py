import cic_assets
import cic_grants
import cic_orgs
import cic_people
import json
import logging
import re
import requests

################################
# pi_migrate_from_drupal
#
# Utility to enhance PI entries by scraping the Drupal web pages
################################

DRUPAL_BASE = 'https://covidinfocommons.datascience.columbia.edu'
HTML_CLEANER = re.compile('<.*?>') 
HREF_RE = re.compile('href=[\'"]?([^\'" >]+)')
SRC_RE = re.compile('src=[\'"]?([^\'" >]+)')
ORCID_RE = re.compile('(\d\d\d\d)-*(\d\d\d\d)-*(\d\d\d\d)-*(\d\d\d.)')

def clean_html(raw_html):
  cleantext = re.sub(HTML_CLEANER, '', raw_html)  
  return cleantext.strip()


def get_href(raw_html):
  srctext = re.search(HREF_RE, raw_html)
  if srctext is None:
    return ''
  else:
    return srctext.group(1)


def get_src(raw_html):
  srctext = re.search(SRC_RE, raw_html)
  if srctext is None:
    return ''
  else:
    return srctext.group(1)


def process(person):
    meta = person['attributes']
    if meta is None:
        return
    if meta['private_emails'] is not None and len(meta['private_emails']) > 0:
        print(f"email {meta['private_emails']}")
        if 'https://covidinfocommons' not in meta['private_emails']:
            print(" -- skipping")
            return
        response = requests.get(meta['private_emails'])
        json = build_person_json(response.text, int(person['id']))
        # Update the person
        cic_people.update_cic_person(json, person['id'])
        
def get_values(html, field_head):
    lines = html.splitlines()
    for idx,line in enumerate(lines):
        if field_head in line:
            print(f" found head #{idx} -- {line}")
            found = []
            for i in range(idx+1, len(lines)):
                if "/section" in lines[i]:
                    break
                cl = clean_html(lines[i])
                if len(cl) >= 2:
                    found.append(cl)
            print(found)
            return found

            
def get_urls(html, field_head):
    lines = html.splitlines()
    for idx,line in enumerate(lines):
        if field_head in line:
            print(f" found head #{idx} -- {line}")
            found = []
            for i in range(idx+1, len(lines)):
                if "/section" in lines[i]:
                    break
                cl = get_href(lines[i])
                if len(cl) >= 2:
                    found.append(cl)
            print(found)
            found

            
def get_image_url(html, field_head):
    lines = html.splitlines()
    for idx,line in enumerate(lines):
        if field_head in line:
            print(f" found head #{idx} -- {line}")
            found = []
            for i in range(idx+1, len(lines)):
                if "/aside" in lines[i] or "/section" in lines[i]:
                    break
                cl = get_src(lines[i])
                if len(cl) >= 2:
                    found.append(cl)
            print(found)
            return found

        
def parsit(html):
    lines = html.splitlines()
    for idx,line in enumerate(lines):
        if 'Awarded COVID' in line:
            print(f" found line #{idx} -- {line}")
            print(f" nextline == {lines[idx + 2]}")
     

def build_person_json(html, pi_id):
  person_data = {
    "data": {
      "type": "Person",
      "attributes": {
        "private_emails": "" # remove the private_emails
      }}}
  
  orcid = get_values(html, 'ORCID ID:')
  if orcid is not None:
    orcid = standardize_orcid(orcid[0])
    person_data['data']['attributes']['orcid'] = orcid    
  websites = get_values(html, 'Professional Website(s):')
  proj_websites = get_values(html, 'Project-Related Website(s):')
  if proj_websites is not None:
    if websites is None:
      websites = proj_websites
    else:
      websites = websites + proj_websites
  if websites is not None:
    person_data['data']['attributes']['websites'] = websites
  profile_image = get_image_url(html, 'col-md-2 pull-right')
  if profile_image is not None and len(profile_image) > 0:
    profile_image = DRUPAL_BASE + profile_image[0]
    cic_assets.find_or_create_for_person('profile_image', profile_image, pi_id)
    
  video = get_image_url(html, 'Video:')
  if video is not None and len(video) > 0:
    cic_assets.find_or_create_for_person('cic_video', video[0], pi_id)
  
  # grants = get_urls(html, 'Awarded COVID Grants:')
  # ignored_output_keywords = get_values(html, 'Expected Research Output:')
  # ignored_proj_keywords = get_values(html, 'Project Keywords:')
  keywords = get_values(html, "PI's Area(s) of Scientific Expertise:")
  if keywords is not None:
    person_data['data']['attributes']['keywords'] = keywords[0].split(',')

  print(f"Person update data: {person_data}")
  return person_data


def standardize_orcid(st):
  if 'https://orcid' in st:
    # assume it's in full orcid format
    return st.strip()
  elif '-' in st:
    # assume it's formatted with dashes, but is just the numerical part
    return "https://orcid.org/" + st
  else:
    mo = re.match(ORCID_RE, st)
    if mo is None:
      return None
    return "https://orcid.org/" + mo.group(1) + "-" + mo.group(2) + "-" + mo.group(3) + "-" + mo.group(4)
  
def main():
  # for testing, process just one person
#  p = cic_people.find_cic_person("Khalid K", "Alam")
#  print(p)
#  process(p)
#  return

  # process all people, one page at a time
  page = 1
  total = 0
  people = cic_people.find_cic_people(page)
  print(f"Received {len(people)} people")
  while people is not None and len(people) > 0:
    total += len(people)
    for p in people:
      print(f"Processing {p['id']}")
      process(p)
    page += 1
    people = cic_people.find_cic_people(page)
    if people is not None:
      print(f"Received {len(people)} people -- total {total}")
  print("Completed PI processing")


if __name__ == "__main__":
    main()

