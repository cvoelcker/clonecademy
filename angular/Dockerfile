# Last.Backend angular example image
FROM node:latest

RUN mkdir /angular
WORKDIR /angular

COPY package.json /angular/

RUN apt-get update && apt-get install -y nodejs
RUN npm install --silent -g @angular/cli
RUN npm install --silent ngx-bootstrap --save
RUN npm install --silent


ADD . /angular
