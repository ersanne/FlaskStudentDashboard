FROM python:3.6-alpine

RUN adduser -D studentportal

WORKDIR /home/studentportal

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY studentportal studentportal
COPY run.py config.py boot.sh ./
RUN chmod +x boot.sh

USER studentportal

EXPOSE 5000
ENTRYPOINT [ "./boot.sh" ]