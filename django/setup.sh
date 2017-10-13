#! /bin/bash

python3 /clonecademy/django/manage.py migrate

# python3 /clonecademy/django/manage.py shell -c "import initialize_db"

# cd /clonecademy/angular && npm run ng build

supervisord -n
