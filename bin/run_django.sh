#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"

cd $DIR
cd django

docker-compose run django python manage.py $@
