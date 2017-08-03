#! /bin/bash

python3 /home/docker/django/manage.py migrate 

python3 /home/docker/django/manage.py shell -c "import clonecademy.initialize_db"

supervisord -n
