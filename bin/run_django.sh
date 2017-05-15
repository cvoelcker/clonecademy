#!/bin/bash
DIR=$(find / -type d -name 'clonecadamy' 2>/dev/null -print -quit)

cd $DIR
cd django

docker-compose run django python manage.py $@s
