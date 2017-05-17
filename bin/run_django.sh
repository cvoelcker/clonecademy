#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && dirname $(pwd -P) )"

cd $DIR
cd django

docker-compose run django python manage.py $@
