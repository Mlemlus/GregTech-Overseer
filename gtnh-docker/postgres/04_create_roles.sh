#!/bin/bash

# Run a sql command to create the role with password enviroment variable 
psql -U postgres -d postgres -c "CREATE ROLE gtoverseer_app WITH LOGIN ENCRYPTED PASSWORD '${POSTGRES_PASSWORD}'"