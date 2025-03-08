#!/bin/bash


## THIS IS IN PROGRESS -- slowly adding to it

## MUST have AWS credentials in place -- should add a check for them and exit if not working

export CIC_ENV=dev

echo
echo "Deploying $CIC_ENV"
echo MUST delete https://us-east-1.console.aws.amazon.com/s3/buckets/cuit-infra-cice-dev-s3-static if React content is changed
echo


source ~/covid-infocommons/venv/bin/activate
export NODE_ENV=development
export AWS_PROFILE=cuit-infra-cice-dev
cd ~/covid-infocommons/frontend/search
npm run webpack
cd ~/covid-infocommons/backend
pip install -r requirements.txt
python manage.py collectstatic --noinput

zappa update dev
zappa manage dev "collectstatic --noinput"



# if it's a prod build
# export NODE_ENV=production

# <<< run the update_frontend >>>>

# export AWS_PROFILE=cuit-infra-cice-prod
# python saml.py cuit-dev-role 305803678806
# python saml.py cuit-prod-role 031752658700
# aws sts get-caller-identity
# <<< delete the search folder from the S3 bucket >>>
# zappa manage dev “collectstatic --noinput”

# if schema updates are required
# python manage.py makemigrations
# zappa manage dev migrate
