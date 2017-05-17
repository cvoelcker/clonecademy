#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"

cd $DIR
cd django

docker-compose build
docker-compose run django python3 manage.py migrate
