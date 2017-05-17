#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && dirname $(pwd) )"

cd $DIR
cd django
docker-compose up -d
