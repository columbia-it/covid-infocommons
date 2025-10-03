
Dev scripts/process
======================

- On local, cic_login_credentials.sh
- On AWS console (dev), delete contents of static folder https://us-east-1.console.aws.amazon.com/s3/buckets/cuit-infra-cice-dev-s3-static
- On Django machine, deploy_cic.sh



Prod scripts/process
======================

- On local, prod_cic_login_credentials.sh
- On AWS console (prod), delete contents of static folder https://us-east-1.console.aws.amazon.com/s3/buckets/cuit-infra-cice-prod-s3-static
- On Django machine, prod_deploy_cic.sh


Getting a token for AWS usage
=============================

The token must be obtained on a machine that has a graphical web browser. If the
actual deploy will be performed on a different machine, take the file created by
this process (~/.aws/credentials) and copy it to the other machine.

```
# Ensure the chromedriver executable is first in the path, so it doesn't get clobbered by rbenv's chromedriver
export PATH=/usr/local/bin:$PATH

cd ~/lib/covid-infocommons/backend

### For dev ###
export AWS_PROFILE=cuit-infra-cice-dev
python saml.py cuit-dev-role 305803678806

# copy the credentials file to your deploy server
scp /Users/ryan/.aws/credentials ryan-django:.aws/credentials

# if it complains about the chromedriver version, get a new one from
# https://googlechromelabs.github.io/chrome-for-testing/ (must find the version number of your Chrome
# and get the matching chromedriver)
# save it in /usr/local/bin/chromedriver

# Verify if needed
aws sts get-caller-identity

### For prod ###
export AWS_PROFILE=cuit-infra-cice-prod

# Note that the below command uses "cuit-dev-role", because it's the role
# for developers, not for a "dev" environment
# BUT the numerical part is for the prod environment credentials
python saml.py cuit-dev-role 031752658700


# Verify if needed
aws sts get-caller-identity

# copy the credentials file to your deploy server
scp /Users/ryan/.aws/credentials ryan-django:.aws/credentials


Deploying the CIC code in the CUIT environment
===============================================

Prep:
- ensure you have an AWS token in place (see section above)
- delete files from the AWS S3 static storage

#### MOST OF THIS PROCESS is in deploy_cic.sh -- for the dev server

Basic deployment process:
```
# initialize virtual environment
source ~/covid-infocommons/venv/bin/activate 

### For dev ###
export NODE_ENV=development
export AWS_PROFILE=cuit-infra-cice-dev

### For prod ###
export NODE_ENV=production
export AWS_PROFILE=cuit-infra-cice-prod

# Update static files used by the frontend (including CSS)
# This will put files in backend/search/static
cd ~/covid-infocommons/frontend/search
npm run webpack

# Update backend code, which manages the deploy
cd ~/covid-infocommons/backend
pip install -r requirements.txt
python manage.py collectstatic

# get AWS token if needed
(see below for AWS token information)

# if schema updates are required
# python manage.py makemigrations
# zappa manage dev/prod migrate
 
## Only needed if there are certain types of frontend changes; not sure which ones
## delete files from S3 bucket cuit-infra-cice-dev-s3-static
https://cuit.columbia.edu/aws

## only delete folders that need to be updated

### For dev ###
zappa update dev
# -- if you see "Warning! Couldn't get function cice-dev", that means you need to update the AWS token
zappa manage dev "collectstatic --noinput"
## IMPORTANT -- if the last command has an error (typically caused by a timeout), run it again

### For prod ###
zappa update prod
zappa manage prod "collectstatic --noinput"
## IMPORTANT -- if the last command has an error (typically caused by a timeout), run it again


Lingo4g
=========

Getting to the Lingo box requires contorting through the CUIT system
-- it's stupid. Type `lingo` and enter your columbia password
continually until you get the message that you're in the  Lingo
machine.

To update the index in Lingo:
1. On a machine with CIC API access, export the grants in Lingo-ready
   format (`cic_run.sh lingo_exporter.py`)
2. Get the export file to the lingo machine (e.g., put it at a public
   URL and curl it from the lingo machine)
3. Move the file to `/home/cic2119/lingo/datasets/dataset-cic/data/cic_grants.json`
4. Reindex lingo
```
  cd  /home/cic2119/lingo/datasets/dataset-cic/data/
  curl "http://secundus.datadryad.org/cic_grants.json" >cic_grants.json
  cd /home/cic2119/lingo
  ./l4g index -p datasets/dataset-cic --force
  ./l4g server -p datasets/dataset-cic --port 8080
```


Troubleshooting
===============

```
# get out of the virtual environment
deactivate
# remove the virtual environment and recreate
rm -rf ~/lib/covid-infocommons/venv
cd ~/lib/covid-infocommons
python3 -m venv ./venv

(then start the deploy again)

# look at the logs
zappa tail dev

# try it on a different OS
# you can copy the .aws/configure file to another machine and deploy from there
```


