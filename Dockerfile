FROM ubuntu:18.04
MAINTAINER Erik Sanne <studentportal@eriksanne.com>

# install our dependencies and nodejs
RUN apt-get update && apt-get -y install python-pip python-dev git npm

# Python environment
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

WORKDIR /home/studentportal

# Copy app and startup script
COPY studentportal studentportal
COPY wsgi.py config.py bower.json ./

# install bower
RUN npm install --global bower
# install dependencies
RUN bower install --allow-root

# Run app on port 5000
CMD ["gunicorn", "-b", ":5000", "wsgi:app"]