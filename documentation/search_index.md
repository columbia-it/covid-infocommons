
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


