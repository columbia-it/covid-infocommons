
Search Index
============

The search index is managed in AWS OpenSearch

Updating the index
-------------------

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
pip install opensearch-py
```

Running code:
```
source venv/bin/activate
python search.py 
```

