FROM ubuntu:18.04
MAINTAINER Erik Sanne <studentportal@eriksanne.com>

# install our dependencies and nodejs
RUN apt-get update && RUN apt-get -y install python-pip python-dev
RUN apt-get update && RUN apt-get -y install nodejs

# Python environment
COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

RUN adduser -D studentportal

WORKDIR /home/studentportal

# install bower
RUN npm install --global bower
RUN bower install

# Copy app and startup script
COPY studentportal studentportal
COPY run.py config.py ./
RUN chmod +x boot.sh

# Switch to studentportal user
USER studentportal

# Run app on port 5000
EXPOSE 5000
CMD ["gunicorn", "-b", ":5000", "wsgi:app"]