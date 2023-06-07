#!/bin/sh

date +"%Y/%m/%d %H:%M:%S"

which python3

export CICE_ENV=dev
export AWS_NEW_CRED=yes

if [ "$CICE_ENV" == "dev" ]
then
    export ACS_AWS_ACCOUNT=305803678806
    export AWS_PROFILE=cuit-infra-cice-dev
fi

if [ "$CICE_ENV" == "prod" ]
then
    export ACS_AWS_ACCOUNT=031752658700
    export AWS_PROFILE=cuit-infra-cice-prod
fi

if [ -d "py3_venv" ]
then
    echo virtual env exists. deleting existing virtual env.
    rm -r py3_venv/
fi

git checkout main
git pull

python3 -m venv py3_venv
source py3_venv/bin/activate
pip install -r requirements.txt
pip freeze

###
# Enable the code below for auth once we have the AWS key ID and secret.
# Use the workaround untill then.
###

# if [ $AWS_NEW_CRED == "yes" ]
# then
#   echo "Generating a new AWS credentials"
#   python create_aws_cred.py
# fi

## Workaround 
export PATH=$PATH:/Users/sg3847/Downloads
python saml.py cuit-dev-role 305803678806
aws sts get-caller-identity

python manage.py collectstatic

zappa status $CICE_ENV
zappa update $CICE_ENV
zappa manage $CICE_ENV showmigrations
zappa manage $CICE_ENV migrate
zappa manage $CICE_ENV showmigrations
#zappa manage $CICE_ENV "collectstatic --noinput"

date +"%Y/%m/%d %H:%M:%S"

deactivate