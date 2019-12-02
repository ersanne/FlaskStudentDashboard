FROM mongo
COPY studentportal studentportal

CMD ["mongorestore", "--host", "mongodb", "-d", "studentportal", "--drop", "studentportal"]