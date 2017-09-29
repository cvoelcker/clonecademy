# Last.Backend angular example image
FROM node:8.0.0

RUN mkdir /angular
WORKDIR /angular

COPY package.json /angular/

ADD . /angular

RUN rm -rf angular/node-module

RUN npm i
