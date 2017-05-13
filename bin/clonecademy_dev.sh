#!/bin/bash

#start_django
#start_angular

if [ ! -z $1 ] && [ $1 = "atom" ]
  then
    DIR=$(find / -type d -name 'clonecadamy' 2>/dev/null -print -quit)

    atom $DIR
fi
