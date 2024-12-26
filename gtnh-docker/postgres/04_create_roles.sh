#!/bin/bash
# Run a sql command to create the role with password enviroment variable
psql -U "${POSTGRES_USER}" -d postgres -c "CREATE ROLE gtoverseer_app WITH LOGIN ENCRYPTED PASSWORD '${GTOVERSEER_POSTGRES_PASSWORD}'"