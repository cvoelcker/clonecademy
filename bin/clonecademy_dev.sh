#!/bin/bash

start_django
start_angular

if [ $1 = "atom" ]
  then
    DIR=$(ls -R /home 2>/dev/null | grep "clonecadamy/django:")

    DIR="${DIR%"${DIR##*[!django:]}"}"

    atom $DIR
fi
