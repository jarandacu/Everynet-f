#!/bin/sh

if [ -f initial.sql ]; then
  MYSQL_CONN="-u$MYSQL_USER -p$MYSQL_PWD -h$MYSQL_HOST"
  echo "Wait for MySQL is ready"
  while ! mysqladmin ping $MYSQL_CONN --silent; do
    sleep 1
    echo "Wait..."
  done

  echo "Load inital dump"
  mysql $MYSQL_CONN < initial.sql
  if ! mysql $MYSQL_CONN -e "use $MYSQL_DB"; then
    echo "Error database not created!"
    exit
  fi

  rm -f initial.sql
fi

python main.py

