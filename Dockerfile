FROM ubuntu:17.04

run apt-get update && apt-get upgrade -y && \
    apt-get install -y curl npm python3 python3-pip nginx supervisor pwgen postgresql libpq-dev
run pip3 install -U pip setuptools
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash - && apt-get install -y nodejs
RUN mkdir /clonecademy

workdir /clonecademy

RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY bin/init/sites-available/default /etc/nginx/sites-available/default
COPY bin/init/supervisor-app.conf /etc/supervisor/conf.d/

RUN mkdir /clonecademy/django
ADD ./django /clonecademy/django
add django/requirements.txt /clonecademy/django


workdir /clonecademy/django
RUN pip3 install -r requirements.txt
RUN pip3 install uwsgi
run pip3 freeze


RUN mkdir /clonecademy/angular
add ./angular /clonecademy/angular
workdir /clonecademy/angular/
run npm i
run npm run ng build --prod

workdir /clonecademy/django
add ./bin/init/setup.sh /clonecademy/django/setup.sh


expose 80
