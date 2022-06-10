FROM postgres
COPY init.db.sh /tmp/


LABEL creator="Dawid G."

# RUN psql -U postgres
# RUN CREATE DATABASE testabc
#Ports 3306 33060, to join HOST + 3306
