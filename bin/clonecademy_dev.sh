#!/bin/bash

start_django
start_angular

if hash atom 2>/dev/null; then
  echo "Do you want to start atom in the clonecademy dir? y/N"
  read answer
  if [ $answer == "Y" ] || [ $answer == "y" ]
    then
      DIR=$(dirname $(dirname $(readlink -f ${BASH_SOURCE[0]})))
      atom $DIR
  fi
fi
