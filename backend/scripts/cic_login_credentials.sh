#!/bin/bash 

export PATH=/usr/local/bin:$PATH

cd ~/lib/covid-infocommons/backend

### For dev ###
export AWS_PROFILE=cuit-infra-cice-dev
python3 saml.py cuit-dev-role 305803678806

scp /Users/ryan/.aws/credentials ryan-django:.aws/credentials
