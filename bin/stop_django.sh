#!/bin/bash

docker stop $(docker ps -a -q  --filter ancestor=django-clonecademy:dev)
docker stop $(docker ps -a -q  --filter ancestor=postgres)
