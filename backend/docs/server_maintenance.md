
Server Maintenance
====================


Deploying code updates
========================

The deploy.py script


Managing the search indexes
============================

- Search indexes live in AWS OpenSearch
- All management of the indexes must be performed through AWS Cloud9

Cloud9 setup
-------------

- You must create a Cloud9 instance in the same VPC and subnet as the OpenSearch machine
- In Cloud9's terminal window, install the opensearch library
```
python -m venv venv
source venv/bin/activate
pip install opensearch-py
```

To run index scripts:
- Start Cloud9
- Create a new file and copy/paste one of the scripts from the `backend/scripts` directory
- source venv/bin/activate
- run my_new_file.py

