#!/bin/bash
DIR=$(dirname $(dirname $(readlink -f ${BASH_SOURCE[0]})))

cd $DIR
cd django

docker-compose build
docker-compose run django pyhton3 makemigrations
docker-compose run django python3 manage.py migrate
