#!/bin/bash
DIR=$(dirname $(dirname $(readlink -f ${BASH_SOURCE[0]})))

cd $DIR
cd django
docker-compose up -d
