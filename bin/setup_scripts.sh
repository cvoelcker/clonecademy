#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

#touch tmp

#sed '2 i DIR='$DIR dir.sh > tmp
#cat tmp > dir.sh

#rm tmp

sudo ln -s $DIR"/build_angular.sh" "/usr/bin/build_angular"
sudo ln -s $DIR"/build_django.sh" "/usr/bin/build_django"

sudo ln -s $DIR"/start_angular.sh" "/usr/bin/start_angular"
sudo ln -s $DIR"/start_django.sh" "/usr/bin/start_django"

sudo ln -s $DIR"/stop_angular.sh" "/usr/bin/stop_angular"
sudo ln -s $DIR"/stop_django.sh" "/usr/bin/stop_django"

sudo ln -s $DIR"/clonecademy_build.sh" "/usr/bin/clonecademy_build"
sudo ln -s $DIR"/clonecademy_dev.sh" "/usr/bin/clonecademy_start"
sudo ln -s $DIR"/clonecademy_stop.sh"  "/usr/bin/clonecademy_stop"
