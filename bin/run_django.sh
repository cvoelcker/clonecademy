#!/bin/bash
DIR=$(cd $(dirname $([ -L $0 ] && readlink -f $0 || echo $0)) && dirname $(pwd -P))

cd $DIR
cd django

docker-compose run django python manage.py $@
