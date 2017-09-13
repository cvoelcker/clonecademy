# clonecadamy

This is a project for the iGEM Team at TU Darmstadt build during the summer semester "bachelorpraktikum" of the faculty of Computer Science. The developers are four computer science students currently in the final year of our bachelor studies.

## Installation (development)
If you have self package inside your home folder just go on. Otherwise you have to
To install all run `bin/setup_script.sh`. It installes Docker if required and sets links to the /usr/bin folder to start the images from anywhere.

`clonecademy_build` builds the docker container for angular and django

`clonecademy_start` starts the containers and if you have atom installed you can add atom as parameter. This will open the folder with atom

`clonecademy_stop` stopps all container.

If you want to start, stop or build single parts you can use `start_angular` `stop_angular` `build_angular` `start_django` `stop_django` `build_django`.

## django
To run a script on django you can user `run_django` and add your script. It is simmilar to `python manag.py`

## angular
If you want to run a script on the angular docker use `run_angular`.

# Installation (production)

To install the software on your server, you need to have Docker and docker-compose up to date. The installation script is located in `/install/install.sh`. This script links all files correctly (if you want to build a regular makefile, please feal free to create a pull-request).

You should change all settings in the files:
* `settings.py`: You should change the allowed hosts to your local settings.
* `settings-secret.py`: Change all fields
* `docker-compose.yml`: You should change the path of the linked database. The database will be stored in the provided location on the server iself, so that data is kept, even if the docker container is down.
* `angular/environments/environent.ts`: Change production to true

If you want to run the server, you only need to call `docker-compose up`. This will expose the plattform via port 80. The main page can now be reached via `localhost` and the admin backend of the Django instance via `localhost/api/admin`.

# Update (production)

First, make a backup copy of the database folder. The location was provided by the `docker-compose.yml`. Then, stash your changed files either with git stash or by making a backup copy. If you have kept everything in the git repository, you can quickly check which files have been changed by running `git status`.

Then execute the following commands:
`git pull`
Reload your stashed files.
`./install.sh`
`docker-compose up`

Everything should now ork as expected and run in the current version.
