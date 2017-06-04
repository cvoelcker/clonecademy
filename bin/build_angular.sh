#!/bin/bash
DIR=$(dirname $(dirname $(readlink -f ${BASH_SOURCE[0]})))

cd $DIR
cd angular
docker-compose build
docker-compose run angular npm i -s
