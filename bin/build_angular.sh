#!/bin/bash

DIR=$(find / -type d -name 'clonecadamy' 2>/dev/null -print -quit)

cd $DIR
cd angular
docker-compose build
#docker-compose run angular npm install --silent
