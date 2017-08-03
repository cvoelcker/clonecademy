#!/bin/bash

cp -r ../angular .
cp -r ../django .

cp init/initialize_db.py django/clonecademy
cp init/settings_production.py django/clonecademy
cp init/settings_secret.py django/clonecademy
cp init/wsgi.py django/clonecademy
cp init/manage.py django

rm -r angular/node_modules
rm -r angular/dist

docker-compose build

rm -r angular
rm -r django

