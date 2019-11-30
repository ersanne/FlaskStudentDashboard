#!/bin/sh
source venv/bin/activate
falsk db upgrade
flask translate compile
exec gunicorn -b :5000 --access-logfile - --error-logfile - studentportal:app