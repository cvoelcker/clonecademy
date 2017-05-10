#!/bin/bash

docker stop $(docker ps -a -q  --filter ancestor=angular-clonecademy:dev)
