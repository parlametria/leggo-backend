FROM node:14-alpine

WORKDIR /code

RUN apk --no-cache add curl bash

RUN curl https://cli-assets.heroku.com/install.sh | sh

COPY . .
