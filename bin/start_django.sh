#!/bin/bash

DIR=$(ls -R /home 2>/dev/null | grep "clonecadamy/django:")

DIR="${DIR%"${DIR##*[!:]}"}"

cd $DIR
docker-compose up -d
