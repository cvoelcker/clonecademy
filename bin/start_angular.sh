#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && dirname $(pwd) )"

cd $DIR
cd angular
docker-compose up -d
