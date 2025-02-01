
Deploying the CIC code in the CUIT environment
===============================================

Prep:
- clear files from backend/static and backend/search/static if there are any
- ensure you have an AWS token in place (see section below)

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

## ??Not needed?
## delete files from S3 bucket cuit-infra-cice-dev-s3-static
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


Getting a token for AWS usage
=============================

The token must be obtained on a machine that has a graphical web browser. If the
actual deploy will be performed on a different machine, take the file created by
this process (~/.aws/credentials) and copy it to the other machine.

```
# Ensure the chromedriver executable is first in the path, so it doesn't get clobbered by rbenv's chromedriver
export PATH=/usr/local/bin:$PATH

cd backend

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
python saml.py cuit-dev-role 031752658700


# Verify if needed
aws sts get-caller-identity

# copy the credentials file to your deploy server
scp /Users/ryan/.aws/credentials ryan-django:.aws/credentials

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
