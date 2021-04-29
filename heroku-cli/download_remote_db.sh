#!/usr/bin/env sh

# Recupera banco de dados POSTGRES associado à API no heroku
heroku pg:backups:capture -a $HEROKU_APP_NAME

# Faz o download do dump do banco de dados POSTGRES associado à API no heroku
heroku pg:backups:download -a $HEROKU_APP_NAME -o $DUMP_EXPORT_PATH
