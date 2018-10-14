#!/bin/bash

if [ "$1" == "create" ]; then
  echo "Database Creation"
  mysql -u root -e "CREATE DATABASE IF NOT EXISTS fr"

  echo "Create Env"
  if [ ! -d "env" ]; then
    virtualenv env --python=python3
  fi
fi


if [ "$1" == "create" ] || [ "$1" == "env" ]; then
  echo "Env Setting"
  export SECRET_KEY="123Secret"
  export FLASK_APP=wsgi.py
  export FLASK_ENV=development
  export DEBUG=True
  export CONFIG=configs.development.Dev

  source env/bin/activate
fi


if [ "$1" == "create" ]; then
  echo "Install Requirements"
  pip install -r requirements
fi
