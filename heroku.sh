#!/bin/bash
gunicorn manage:app --daemon
python manage.py runworker
