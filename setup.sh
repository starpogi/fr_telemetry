#!/bin/bash

echo "Database Creation"
mysql -u root -e "CREATE DATABASE IF NOT EXISTS fr"

echo "Env Setting"
export SECRET_KEY="123Secret"
export FLASK_APP=wsgi.py
export FLASK_ENV=development
export DEBUG=True
export CONFIG=configs.development.Dev

echo "Create Env"
if [ ! -d "env" ]; then
  virtualenv env --python=python3
fi

source env/bin/activate

echo "Install Requirements"
pip install -r requirements
