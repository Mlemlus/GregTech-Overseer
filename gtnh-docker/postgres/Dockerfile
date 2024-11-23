FROM postgres:17-bookworm

# get that sweet db script in there
COPY ./postgre_GTOverseer.sql /docker-entrypoint-initdb.d/

# get that gto_app password in here
ARG GTOVERSEER_POSTGRES_PASSWORD

# lets pass the env config into the script
COPY ./env.sh /docker-entrypoint-initdb.d/
RUN chmod +x /docker-entrypoint-initdb.d/env.sh && /docker-entrypoint-initdb.d/env.sh
RUN rm -f /docker-entrypoint-initdb.d/env.sh && rm -f /docker-entrypoint-initdb.d/postgre_GTOverseer.sql
# pass them network restrictions
COPY ./pg_hba.conf /etc/postgresql/pg_hba.conf

# idk why this doesnt work
RUN chown -R postgres:postgres /docker-entrypoint-initdb.d/init.sql
RUN mkdir -pm 700 /db-logs
RUN mkdir -pm 700 /db-backups
RUN chown -R postgres:postgres /db-logs
RUN chown -R postgres:postgres /db-backups

RUN docker-entrypoint.sh
