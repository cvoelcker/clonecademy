#!/bin/bash

start_django
start_angular

# if hash atom 2>/dev/null; then
#   echo "Do you want to start atom in the clonecademy dir? Y/n"
#   read answer
#   if [ ! -z $answer ]
#     then
#     if [ $answer == "n" ] || [ $answer == "N" ]
#       then
#         exit
#     fi
#   fi
#   DIR=$(dirname $(dirname $(readlink -f ${BASH_SOURCE[0]})))
#   atom $DIR
# fi
