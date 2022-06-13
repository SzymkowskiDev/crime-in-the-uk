FROM postgres
COPY init.db.sh /tmp/
# COPY hello.sh /tmp/
ENV POSTGRES_PASSWORD=abc123
LABEL creator="Dawid G."

# RUN sleep 20 && chmod u+x /tmp/hello.sh && bash /tmp/hello.sh
# RUN cd / && mkdir cocacola
# RUN psql -U postgres
# RUN CREATE DATABASE testabc
#Ports 3306 33060, to join HOST + 3306
