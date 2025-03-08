#!/bin/bash

export DB_ENGINE=django.db.backends.mysql
export DB_NAME=cic
export DB_USER=basic
export DB_PASSWORD=password
export DB_HOST=localhost
export DB_PORT=3306

cd ~/covid-infocommons/frontend/search
npm run webpack
