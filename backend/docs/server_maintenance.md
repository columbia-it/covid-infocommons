
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


Database
=========

CIC-E uses MySQL relational database running on AWS as a Aurora MySQL (serveless) survice.

Aurora backs up our cluster volume automatically and retains restore data for the length of the backup retention period which is set to 35 days. Aurora backups are stored in Amazon S3.

We are also keeping a daily snapshot of the data in our cluster volume and we can create a new DB cluster by restoring from a DB snapshot.

Restoring from a snapshot
--------------------------

You can restore a DB cluster from a DB cluster snapshot using the AWS Management Console, the AWS CLI, or the RDS API.

To restore, you provide the name of the DB cluster snapshot to restore from, and then provide a name for the new DB cluster that is created from the restore. You can't restore from a DB cluster snapshot to an existing DB cluster; a new DB cluster is created when you restore.

You can use the restored DB cluster as soon as its status is available.

Using Console
1. Sign in to the AWS Management Console and open the Amazon RDS console at https://console.aws.amazon.com/rds/.
2. In the navigation pane, choose Snapshots.
3. Choose the DB cluster snapshot that you want to restore from.
4. For Actions, choose Restore snapshot.
5. On the Restore snapshot page, for DB instance identifier, enter the name for your restored DB cluster.
6. Specify other settings.
7. For information about each setting, see Settings for Aurora DB clusters.
8. Choose Restore DB cluster.

CUIT process for DB recovery

The database recovery can be done only by the DevOps or DBA teams as they have the necessary permissions in AWS to perform the backup and recovery operations. In order to request DB recovery, we need to open a new service request in ServiceNow and assign it to the DBA group. Mention the DB cluster name, AWS account number and the date and time of the snapshot that the data needs to be recovered from. 
