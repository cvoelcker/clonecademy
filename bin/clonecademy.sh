#!/bin/bash

DIR=$(dirname $(dirname $(readlink -f ${BASH_SOURCE[0]})))

function help {
echo "info";
echo "-s | start    to start the $1";
echo "-p | pause    to stop the $1";
echo "-b | build    to build the $1";
echo "-rm | remove  remove the docker $1";
}

function startAngular {
	cd $DIR/angular
	docker-compose up -d
}

function startDjango {
	cd $DIR/django
	docker-compose up -d
}

function stopAngular {
	docker 2>/dev/null stop $(docker ps -a -q  --filter name=angular)
	if [ $? == 1 ]
		then
			noBuildError "angular"
	fi
}

function stopDjango {
	docker 2>/dev/null stop $(docker ps -a -q  --filter name=django)
	if [ $? == 1 ]
		then
			noBuildError "django"
	fi
}

function removeAngular {
	docker 2>/dev/null rm $(docker ps -aq -f name=angular)
	if [ $? == 1 ]
		then
			noBuildError "angular"
	fi
}

function removeDjango {
	docker 2>/dev/null rm $(docker ps -aq -f name=django)
	if [ $? == 1 ]
		then
			noBuildError "django"
	fi
}

function buildAngular {
	cd $DIR/angular
	docker-compose build
}

function buildDjango {
	cd $DIR/django
	docker-compose build
	docker-compose run django python3 manage.py makemigrations

	docker-compose run django python3 manage.py makemigrations learning_base

	docker-compose run django python3 manage.py migrate
}

function noBuildError {
	echo "someting went wrong."
	echo "is the"$1"container installed."
	echo "Run 'clonecademy build' or 'clonecademy "$1" build' to start build this container"
}

function runAngular {
	cd $DIR/angular
	docker-compose run angular $@
}

function runDjango {
	cd $DIR/django
	docker-compose run django python manage.py $@
}

function testAngular {
	cd $DIR/angular
	DATE=`date +%Y-%m-%d`
	docker-compose run angular npm test
}

case $1 in
	-h | help)
		help "containers"
		echo "angular       to run the command only in the angular container"
		echo "django        to run the command only in the django container"
	;;
	-s | start)
		startAngular
		startDjango
	;;
	-p | pause)
		stopAngular
		stopDjango
	;;
	-b | build)
		buildAngular
		buildDjango
	;;
	-rm | remove)
		removeAngular
		removeDjango
	;;
	-t | test)
		testAngular
	;;
	angular)
		case $2 in
			-s | start)
			startAngular
			;;
			-p | pause)
			stopAngular
			;;
			-rm | remove)
			removeAngular
			;;
			-b | build)
			buildAngular
			;;
			-h | help)
			help "angular"
			echo "-r | run [command]  run the command in the angular container ";
			;;
			-r | run)
			runAngular ${*:3}
			;;
			-t | test)
			testAngular
			;;
			*)
			startAngular
			;;
		esac
	;;
	django)
		case $2 in
			-s | start)
			startDjango
			;;
			-p | pause)
			stopDjango
			;;
			-rm | remove)
			removeDjango
			;;
			-b | build)
			buildDjango
			;;
			-h | help)
			help "django"
			echo "-r | run [command]  run the command in the django container ";
			;;
			-r | run)
			runDjango ${*:3}
			;;
			*)
			startDjango
			;;
		esac
	;;
	*)
		help "containers"
	;;
esac
