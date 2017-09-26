cd ../../django
rm database/db.sqlite.3
./manage.py migrate
./manage.py loaddata testdata/testdata.json

cd ../angular/tests/protractor
protractor conf.js
