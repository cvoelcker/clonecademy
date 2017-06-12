#!/bin/bash
DIR=$(dirname $(dirname $(readlink -f ${BASH_SOURCE[0]})))

cd $DIR
cd django

docker-compose build
docker-compose run django python3 manage.py makemigrations

docker-compose run django python3 manage.py makemigrations learning_base
docker-compose run django python3 manage.py makemigrations user_model

docker-compose run django python3 manage.py migrate


docker-compose run django python3 manage.py createsuperuser --username admin
docker-compose run django python3 manage.py shell < install_script.py
