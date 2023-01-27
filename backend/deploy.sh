#!/bin/sh

date +"%Y/%m/%d %H:%M:%S"

source venv/bin/activate

# Verify Python version
which python
python -V

# Install dependencies
ls -al
pip install -r requirements.txt
pip freeze

# Set AWS related environment variables
export CICE_AWS_ENV=dev
echo $CICE_AWS_ENV
export CICE_AWS_ACCOUNT=305803678806
echo $CICE_AWS_ACCOUNT
export AWS_PROFILE=cuit-infra-cice-dev
export PATH=$PATH:/Users/sg3847/Downloads
export UPDATE_STATIC=false

# Verify AWS credentials
python saml.py cuit-dev-role 305803678806

# Update Lambda
zappa status $CICE_AWS_ENV
zappa update $CICE_AWS_ENV
zappa manage $CICE_AWS_ENV showmigrations models
zappa manage $CICE_AWS_ENV migrate models
zappa manage $CICE_AWS_ENV showmigrations models
if [ $UPDATE_STATIC ]
then
  echo "Updating static files"
  # Collect static files
  ls -al static/
  python manage.py collectstatic --noinput
  ls -al static/
  zappa manage $CICE_AWS_ENV "collectstatic --noinput"
fi
date +"%Y/%m/%d %H:%M:%S"