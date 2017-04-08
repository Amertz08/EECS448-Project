#!/bin/bash
PYTHON_DIR=/Users/adammertz/.virtualenvs/EEC448-proj/bin
${PYTHON_DIR}/python app/manage.py db migrate
${PYTHON_DIR}/python app/manage.py db upgrade
echo "DONE!"