FROM mongo
COPY studentportal studentportal

CMD ["mongorestore", "--host", "mongodb", "-d", "studentportal", "--authenticationDatabase", "admin", "-u", "mongo_user", "-p", "mongo_secret", "--drop", "studentportal"]