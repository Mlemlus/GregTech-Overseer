FROM postgres:17-bookworm

# copy the scripts
COPY *.sql /docker-entrypoint-initdb.d/
COPY *.sh /docker-entrypoint-initdb.d/

# pass them network restrictions
COPY ./pg_hba.conf /etc/postgresql/pg_hba.conf

RUN docker-entrypoint.sh
