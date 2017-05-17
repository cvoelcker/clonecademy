#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"

cd $DIR
cd angular
docker-compose build
docker-compose run angular npm install --silent
