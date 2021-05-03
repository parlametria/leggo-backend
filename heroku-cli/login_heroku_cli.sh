#!/usr/bin/env sh

# Remove versão anterior da HEROKU API KEY
unset HEROKU_API_KEY

# Abre prompt para login no heroku
heroku login -i

# Exibe Heroku API KEY
heroku auth:token
