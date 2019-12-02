FROM mongo
COPY studentportal-dump studentportal-dump

CMD ["mongorestore", "--host", "mongodb", "--drop", "/mongo-seed/studentportal-dump"]