#!/bin/bash

DIR=$(ls -R /home 2>/dev/null | grep "clonecadamy/angular:")

DIR="${DIR%"${DIR##*[!:]}"}"

cd $DIR

docker-compose build
