#!/bin/bash

echo
echo "Running harvester"
echo

export DB_ENGINE=django.db.backends.mysql
export DB_NAME=cic
export DB_USER=basic
export DB_PASSWORD=password
export DB_HOST=localhost
export DB_PORT=3306

cd ~/covid-infocommons/harvester
source /home/ubuntu/covid-infocommons/venv/bin/activate
/home/ubuntu/covid-infocommons/venv/bin/python nsf_harvester.py
