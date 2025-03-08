#!/bin/bash

echo
echo "Running $1"
echo

export DB_ENGINE=django.db.backends.mysql
export DB_NAME=cic
export DB_USER=basic
export DB_PASSWORD=password
export DB_HOST=localhost
export DB_PORT=3306

source /home/ubuntu/covid-infocommons/venv/bin/activate
cd ~/covid-infocommons/harvester
/home/ubuntu/covid-infocommons/venv/bin/python "$@"
