#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"

cd $DIR
cd angular
docker-compose up -d
