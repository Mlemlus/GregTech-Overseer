------- PRIVILEGES -----------
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
DROP SCHEMA IF EXISTS public CASCADE;

GRANT CONNECT ON DATABASE postgres TO gtoverseer_app;
GRANT USAGE ON SCHEMA "gtoverseer" TO gtoverseer_app;
GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA "gtoverseer" TO gtoverseer_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA "gtoverseer" TO gtoverseer_app;

REVOKE INSERT, UPDATE, DELETE ON "gtoverseer"."tier" FROM gtoverseer_app;
REVOKE INSERT, UPDATE, DELETE ON "gtoverseer"."maintenance" FROM gtoverseer_app;
REVOKE UPDATE, DELETE ON "gtoverseer"."log" FROM gtoverseer_app;
REVOKE DELETE ON "gtoverseer"."machine_maintenance" FROM gtoverseer_app;
REVOKE DELETE ON "gtoverseer"."work" FROM gtoverseer_app;
REVOKE DELETE ON "gtoverseer"."coord" FROM gtoverseer_app;
REVOKE DELETE ON "gtoverseer"."power_source" FROM gtoverseer_app;
