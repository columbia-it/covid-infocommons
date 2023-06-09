#!/bin/bash 
date +"%Y/%m/%d %H:%M:%S"

which python3
python3 -V

python3 -m venv py3_venv
source py3_venv/bin/activate

pwd
pip install -r requirements.txt
python manage.py test --pattern="test_*.py"

#python manage.py collectstatic --noinput
if [ $AWS_NEW_CRED == "Yes" ]
then
  echo "Generating a new AWS credentials"
  python create_aws_creds.py
fi
ls -al ~/.aws/

zappa status $CICE_ENV
zappa update $CICE_ENV
