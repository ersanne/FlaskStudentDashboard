FROM python:3.7-alpine

RUN adduser -D studentportal

WORKDIR /home/studentportal

# Python environment
COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

# Copy app and startup script
COPY studentportal studentportal
COPY run.py config.py boot.sh ./
RUN chmod +x boot.sh

# Switch to studentportal user
USER studentportal

# Install other dependencies
RUN npm install
RUN bower install

# Run app on port 5000
EXPOSE 5000
ENTRYPOINT [ "./boot.sh" ]