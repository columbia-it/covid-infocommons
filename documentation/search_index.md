
Search Index
============

The search index is managed in AWS OpenSearch

Configuration
--------------

Each environment connects to its own OpenSearch cluster: If you login
into aws, lambda, configuration and environment variables, it has the
open search cluster name there. Also, each of the cic-e aws accounts
should have an open search cluster used by their respective lambdas


Updating the index
-------------------

Use the Cloud9 environment to connect to the OpenSearch index:
- Login to AWS - https://www.cuit.columbia.edu/aws -> AWS account login
- From Services, select Cloud9
- Select "connect-to-cice-os-cluster" environment
- Click "Open in Cloud9"

Once the environment is open and ready, you can see and access the existing python scripts in the environment. You can create and run new scripts here as well.
For e.g, there is a script called "update_all_pis.py" which updates all the documents in the index with latest PI data. To run this script -
Activate the existing virtual environment called "venv" using the command `source venv/bin/activate`
Run the script using the command: `python update_all_pis.py`


The index must be accesed through a CUIT AWS account, using the Cloud9 editing
environment.

Hostname should be set to the search cluster's Domain endpoint (VPC).

All commands must be run through the bash shell at the bottom of Cloud9.

First-time setup:
- create a Cloud9 environment in the CIC AWS account
- the environment must use an SSH connection
- run the environment, and in the bash window at the bottom, run:
```
python -m venv venv
source venv/bin/activate
pip install opensearch-py
```

Running code:
```
source venv/bin/activate
python search.py 
```

Sample queries
----------------

For any
```
 query_body = {
      "query": {
            "match_all" :  {}
        }
     }
```

For grants
```
 query_body = {
      "query": {
            "match": {
                "principal_investigator.id": 24773
            }
        }
     }
```

For datasets
```
query_body = {
      "query": {
            "match": {
                "doi": "10.35482/bld.06.2019"
                 #"title": "Cornus"
            }
        }
     }

 query_body = {
      "query": {
            'multi_match': {
                'query': "Weather",
                'operator': 'and',
                'fields': [
                    'doi', 
                    'title', 
                    'abstract',
                    'mime_type', 
                    'keywords', 
                    'awardee_organization.name'
                    'authors.full_name'
                ]
            }
        }
     }
```
