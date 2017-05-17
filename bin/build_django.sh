#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && dirname $(pwd -P) )"

cd $DIR
cd django

docker-compose build
docker-compose run django python3 manage.py migrate
