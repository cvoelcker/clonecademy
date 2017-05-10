#!/bin/bash

docker stop $(docker ps -a -q  --filter ancestor=django-clonecademy:dev)
