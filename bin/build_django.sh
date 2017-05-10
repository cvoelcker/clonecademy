#!/bin/bash

DIR="/home/leonhard/Uni/17_Sommer/BP/local"

cd $DIR
cd django/
docker-compose build
docker-compose run django python3 manage.py migrate
