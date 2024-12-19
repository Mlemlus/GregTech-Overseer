#!/bin/bash

gtoverseer_sql="/docker-entrypoint-initdb.d/postgre_GTOverseer.sql"
init_sql="/docker-entrypoint-initdb.d/init.sql"

echo "GTOVERSEER_POSTGRES_PASSWORD: $GTOVERSEER_POSTGRES_PASSWORD"

if [[ -f "$gtoverseer_sql" ]]; then
  # replace the password var in gtoverseer_sql
  sed "s/\${GTOVERSEER_POSTGRES_PASSWORD}/${GTOVERSEER_POSTGRES_PASSWORD}/g" "$gtoverseer_sql" > "$init_sql"
else
  echo "No postgre_GTOverseer.sql file found" 
  exit 1
fi
