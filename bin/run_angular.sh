#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && dirname $(pwd -P) )"

cd $DIR
cd angular

docker-compose run angular $@
