# clonecadamy

## Installation
If you have this package inside your home folder just go on. Otherwise you have to
To install all run `bin/setup_script.sh`. It installes Docker if required and sets links to the /usr/bin folder to start the images from anywhere.

`clonecademy_build` builds the docker container for angular and django

`clonecademy_start` starts the containers and if you have atom installed you can add atom as parameter. This will open the folder with atom

`clonecademy_stop` stopps all container.

If you want to start, stop or build single parts you can use `start_angular` `stop_angular` `build_angular` `start_django` `stop_django` `build_django`.

## django
To run a script on django you can user `run_django` and add your script. It is simmilar to `python manag.py`

## angular
If you want to run a script on the angular docker use `run_angular`.
