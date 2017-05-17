#!/bin/bash
DIR=$(cd $(dirname $([ -L $0 ] && readlink -f $0 || echo $0)) && dirname $(pwd -P))

echo $DIR

cd $DIR
cd angular
docker-compose up -d
