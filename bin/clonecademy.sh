#!/bin/bash

DIR=$(dirname $(dirname $(readlink -f ${BASH_SOURCE[0]})))

function help {
echo "info";
echo "-s | start    to start the $1";
echo "-p | pause    to stop the $1";
echo "-b | build    to build the $1";
echo "-rm | remove  remove the docker $1";
}

cd $DIR

function testAngular {
	docker-compose run angular npm test
}

function testAngular {
	docker-compose run django python3 /clonecademy/django/manage.py test
}

case $1 in
	-h | help)
		help "containers"
		echo "angular       to run the command only in the angular container"
		echo "django        to run the command only in the django container"
	;;
	-s | start)
		docker-compose up -d
	;;
	-p | pause)
		docker-compose stop
	;;
	-b | build)
		docker-compose build
	;;
	-rm | remove)
		docker-compose rm -f
	;;
	-t | test)
		testAngular
		testDjango
	;;
	angular)
		case $2 in
			-s | start)
			docker-compose up angular
			;;
			-p | pause)
			docker-compose stop angular
			;;
			-rm | remove)
			docker-compose rm -f angular
			;;
			-b | build)
			docker-compose build angular
			;;
			-i | install)
			docker-compose run angular npm run ng build --prod
			;;
			-h | help)
			help "angular"
			echo "-r | run [command]  run the command in the angular container ";
			;;
			-r | run)
			docker-compose run angular ${*:3}
			;;
			-t | test)
			testAngular
			;;
			*)
			docker-compose up angular
			;;
		esac
	;;
	django)
		case $2 in
			-s | start)
			docker-compose start django
			;;
			-p | pause)
			docker-compose stop django
			;;
			-rm | remove)
			docker-compose rm -f django
			;;
			-b | build)
			docker-compose build django
			;;
			-h | help)
			help "django"
			echo "-r | run [command]  run the command in the django container ";
			;;
			-r | run)
			docker-compose run django python3 manage.py ${*:3}
			;;
			*)
			docker-compose up
			;;
		esac
	;;
	*)
		help containers
		echo "angular       to run the command only in the angular container"
		echo "django        to run the command only in the django container"
	;;
esac
