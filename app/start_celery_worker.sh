#!/usr/bin/env bash


/Users/adammertz/.virtualenvs/EEC448-proj/bin/celery worker -A celery_worker.celery --loglevel=info
