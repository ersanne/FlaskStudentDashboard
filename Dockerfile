FROM python:3.7-alpine
MAINTAINER Erik Sanne <studentportal@eriksanne.com>

# Python environment
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

WORKDIR /home/studentportal

# Copy app and config/startup files
COPY studentportal studentportal
COPY wsgi.py config.py bower.json ./

# Run app on port 5000
EXPOSE 5000
CMD ["gunicorn", "-b", ":5000", "wsgi:app"]
