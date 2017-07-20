#!/bin/bash


if [ "$(id -u)" != "0" ]; then
  echo "permissions error: run this script as root user"
  exit
fi


if ! hash docker-compose 2>/dev/null; then
  apt-get remove docker docker-engine
  apt-get update
  apt-get install -y linux-image-extra-$(uname -r) linux-image-extra-virtual
  apt-get install -y apt-transport-https ca-certificates curl software-properties-common
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
  if [[ $(uname -m) == *'64' ]]; then
    add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
 else
   add-apt-repository \
   "deb [arch=armhf] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
 fi
 apt-get update
 apt-get install -y docker docker-compose
fi

echo "do you want to install the scripts to your local bin folder"
echo "[y/N]"
read confirm

share="/usr/local/bin"

# leftover from the old install script
rm 2>/dev/null $share/run_*
rm 2>/dev/null $share/start_*
rm 2>/dev/null $share/build_*
rm 2>/dev/null $share/stop_*
rm 2>/dev/null $share/clonecademy_*

if [ $confirm == "y" ] ||  [ $confirm == "Y" ]
  then

  DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

  rm 2>/dev/null $share/clonecademy
  chmod +x $DIR"/clonecademy.sh"
  ln -s $DIR"/clonecademy.sh" $share/clonecademy

  cp $DIR/clonecademy_autocomplete /etc/bash_completion.d/clonecademy_autocomplete
  echo "you can start the containers with clonecademy start"
  echo "to get more information run clonecademy help"
  echo ""
fi

echo "you have to be member of the docker group or run all scripts as root"
echo "run: sudo usermod -a -G docker your-user-name"
