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
 sudo apt-get install -y docker docker-compose
fi

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

share="/usr/local/bin"

rm 2>/dev/null $share/build_*
sudo chmod +x $DIR/build_*
sudo ln -s $DIR"/build_angular.sh" $share/build_angular
sudo ln -s $DIR"/build_django.sh" $share/build_django

rm 2>/dev/null $share/start_*
sudo chmod +x $DIR/start_*
sudo ln -s $DIR"/start_angular.sh" $share/start_angular
sudo ln -s $DIR"/start_django.sh" $share/start_django

rm 2>/dev/null $share/stop_*
sudo chmod +x $DIR/stop_*
sudo ln -s $DIR"/stop_angular.sh" $share/stop_angular
sudo ln -s $DIR"/stop_django.sh" $share/stop_django

rm 2>/dev/null $share/run_*
sudo chmod +x $DIR/run_*
sudo ln -s $DIR"/run_angular.sh" $share/run_angular
sudo ln -s $DIR"/run_django.sh" $share/run_django

rm 2>/dev/null $share/clonecademy_*
sudo chmod +x $DIR/clonecademy_*
sudo ln -s $DIR"/clonecademy_build.sh" $share/clonecademy_build
sudo ln -s $DIR"/clonecademy_dev.sh" $share/clonecademy_start
sudo ln -s $DIR"/clonecademy_stop.sh"  $share/clonecademy_stop

echo "you have to be member of the docker group or run all scripts as root \n"
echo "run: sudo usermod -a -G docker your-user-name"
