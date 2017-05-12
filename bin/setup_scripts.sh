#!/bin/bash


if [ "$(id -u)" != "0" ]; then
  echo "permissions error: run this script as root user"
  exit
fi


if ! hash docker-compose 2>/dev/null; then
  sudo apt-get remove docker docker-engine
  sudo apt-get update
  sudo apt-get install -y linux-image-extra-$(uname -r) linux-image-extra-virtual
  sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
  if [[ $(uname -m) == *'64' ]]; then
    sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
 else
   sudo add-apt-repository \
   "deb [arch=armhf] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
 fi
 sudo apt-get update
 sudo apt-get install -y docker-ce docker-compose
fi

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

rm 2>/dev/null /usr/bin/build_*
sudo ln -s $DIR"/build_angular.sh" "/usr/bin/build_angular"
sudo ln -s $DIR"/build_django.sh" "/usr/bin/build_django"

rm 2>/dev/null /usr/bin/start_*
sudo ln -s $DIR"/start_angular.sh" "/usr/bin/start_angular"
sudo ln -s $DIR"/start_django.sh" "/usr/bin/start_django"

rm 2>/dev/null /usr/bin/stop_*
sudo ln -s $DIR"/stop_angular.sh" "/usr/bin/stop_angular"
sudo ln -s $DIR"/stop_django.sh" "/usr/bin/stop_django"

rm 2>/dev/null /usr/bin/run*
sudo ln -s $DIR"/run_angular.sh" "/usr/bin/run_angular"
sudo ln -s $DIR"/run_django.sh" "/usr/bin/run_django"

rm 2>/dev/null /usr/bin/clonecademy_*
sudo ln -s $DIR"/clonecademy_build.sh" "/usr/bin/clonecademy_build"
sudo ln -s $DIR"/clonecademy_dev.sh" "/usr/bin/clonecademy_start"
sudo ln -s $DIR"/clonecademy_stop.sh"  "/usr/bin/clonecademy_stop"
