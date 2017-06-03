# Last.Backend angular example image
FROM node:7.10.0

RUN mkdir /angular
WORKDIR /angular

COPY package.json /angular/

RUN apt-get update && apt-get install -y nodejs
RUN npm install --silent -g @angular/cli --save
RUN npm install --silent bootstrap --save
RUN npm install --silent angular2-cookie --save
RUN npm install --silent angular2-jwt --save
RUN npm install --silent


ADD . /angular
