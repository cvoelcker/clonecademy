# Last.Backend angular example image
FROM node:7.10.0

RUN mkdir /angular
WORKDIR /angular

COPY package.json /angular/

RUN npm install -g -s @angular/cli

ADD . /angular
