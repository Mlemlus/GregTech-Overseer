FROM postgres:17-bookworm

# copy the scripts
COPY *.sql /docker-entrypoint-initdb.d/
COPY *.sh /docker-entrypoint-initdb.d/

# pass them network restrictions
COPY ./pg_hba.conf /etc/postgresql/pg_hba.conf

# get those certs
COPY ./ssl /etc/postgresql/ssl
# Set those permissions
RUN chown -R postgres:postgres /etc/postgresql/ssl
RUN chmod 700 /etc/postgresql/ssl
RUN chmod og-rwx /etc/postgresql/ssl/server.crt
RUN chmod og-rwx /etc/postgresql/ssl/server.key

# # idk why this doesnt work
# RUN chown -R postgres:postgres init.sql
# RUN mkdir -pm 700 /db-logs
# RUN mkdir -pm 700 /db-backups
# RUN chown -R postgres:postgres /db-logs
# RUN chown -R postgres:postgres /db-backups

RUN docker-entrypoint.sh
