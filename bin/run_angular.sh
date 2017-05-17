#!/bin/bash
DIR=$(cd $(dirname $([ -L $0 ] && readlink -f $0 || echo $0)) && dirname $(pwd -P))

cd $DIR
cd angular

docker-compose run angular $@
