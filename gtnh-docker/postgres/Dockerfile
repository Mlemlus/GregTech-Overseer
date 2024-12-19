FROM postgres:17-bookworm

# set workdir
WORKDIR /docker-entrypoint-initdb.d

# get that sweet db script in there
COPY ./postgre_GTOverseer.sql .

# get that gto_app password in here
ARG GTOVERSEER_POSTGRES_PASSWORD

# lets pass the env config into the script
COPY env_config.sh .
RUN ls -l /docker-entrypoint-initdb.d
RUN chmod +x env_config.sh
RUN env_config.sh
RUN rm -f env_config.sh && rm -f postgre_GTOverseer.sql
# pass them network restrictions
COPY ./pg_hba.conf /etc/postgresql/pg_hba.conf

# idk why this doesnt work
RUN chown -R postgres:postgres init.sql
RUN mkdir -pm 700 /db-logs
RUN mkdir -pm 700 /db-backups
RUN chown -R postgres:postgres /db-logs
RUN chown -R postgres:postgres /db-backups

RUN docker-entrypoint.sh
