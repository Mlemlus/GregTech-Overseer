--------- DDL ---------
DROP SCHEMA IF EXISTS "gtoverseer" CASCADE;
CREATE SCHEMA "gtoverseer";

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA "gtoverseer";
CREATE EXTENSION IF NOT EXISTS unaccent WITH SCHEMA "gtoverseer";


CREATE TABLE "gtoverseer"."oc_computer" (
	"ID"			SERIAL PRIMARY KEY,
	"oc_address"	CHAR(36) NOT NULL UNIQUE,
	"custom_name"	VARCHAR(50)
);

CREATE TABLE "gtoverseer"."tier" (
	"ID"		SERIAL	PRIMARY KEY,
	"name"		VARCHAR(3) NOT NULL UNIQUE,
	"eu"		INT NOT NULL UNIQUE
);

CREATE TABLE "gtoverseer"."maintenance" (
	"ID"		SERIAL PRIMARY KEY,
	"message"	VARCHAR(30) NOT NULL UNIQUE,
	"tool"		VARCHAR(20) NOT NULL
);
 
CREATE TABLE "gtoverseer"."privilege" (
	"ID"		SERIAL PRIMARY KEY,
	"name"		VARCHAR(30) NOT NULL UNIQUE
);

CREATE TABLE "gtoverseer"."user" (
	"ID"				SERIAL PRIMARY KEY,
	"nickname"			VARCHAR(50) NOT NULL UNIQUE,
	"email"				BYTEA UNIQUE,
	"password_hash"		CHAR(60)
);

CREATE TABLE "gtoverseer"."log" (
	"ID"		SERIAL PRIMARY KEY,
	"time"		TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	"text"		VARCHAR(255) NOT NULL,
	"user_ID"	INT,

	FOREIGN KEY ("user_ID") REFERENCES "gtoverseer"."user"("ID") ON DELETE SET NULL
);

CREATE TABLE "gtoverseer"."cable" (
	"ID"		SERIAL PRIMARY KEY,
	"name"		VARCHAR(50) NOT NULL UNIQUE,
	"density"	SMALLINT NOT NULL,
	"tier_ID"	INT NOT NULL,
	"max_amp"	INT NOT NULL,
	"loss"		SMALLINT NOT NULL,

	FOREIGN KEY ("tier_ID") REFERENCES "gtoverseer"."tier"("ID") ON DELETE CASCADE
);

CREATE TABLE "gtoverseer"."power_network" (
	"ID"				SERIAL PRIMARY KEY,
	"name"				VARCHAR(50) NOT NULL UNIQUE,
	"cable_ID"			INT NOT NULL,
	"owner_ID"			INT,
	"avg_amp"			DECIMAL(12,2),
	"avg_eu"			DECIMAL(22,2),
	"created_at"		TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,

	FOREIGN KEY ("cable_ID") REFERENCES "gtoverseer"."cable"("ID") ON DELETE CASCADE,
	FOREIGN KEY ("owner_ID") REFERENCES "gtoverseer"."user"("ID") ON DELETE SET NULL
);

CREATE TABLE "gtoverseer"."user_privilege" (
	"ID"				SERIAL PRIMARY KEY,
	"user_ID"			INT NOT NULL,
	"privilege_ID"		INT NOT NULL,
	"is_shareable"		BOOLEAN NOT NULL DEFAULT FALSE,

	FOREIGN KEY ("user_ID") REFERENCES "gtoverseer"."user"("ID") ON DELETE CASCADE,
	FOREIGN KEY ("privilege_ID") REFERENCES "gtoverseer"."privilege"("ID") ON DELETE CASCADE
);

CREATE TABLE "gtoverseer"."machine" (
	"ID"					SERIAL PRIMARY KEY,
	"oc_computer_ID" 		INT,
	"tier_ID"				INT NOT NULL,
	"power_network_ID"		INT,
	"owner_ID"				INT,
	"oc_address"			CHAR(36) NOT NULL UNIQUE,
	"name"					VARCHAR(100) NOT NULL,
	"custom_name"			VARCHAR(100),
	"amp"					SMALLINT NOT NULL,
	"created_at"			TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
	"note"					TEXT,
	"is_connected"			BOOLEAN NOT NULL DEFAULT TRUE,

	FOREIGN KEY ("oc_computer_ID") REFERENCES "gtoverseer"."oc_computer"("ID") ON DELETE SET NULL,
	FOREIGN KEY ("tier_ID") REFERENCES "gtoverseer"."tier"("ID") ON DELETE CASCADE,
	FOREIGN KEY ("power_network_ID") REFERENCES "gtoverseer"."power_network"("ID") ON DELETE SET NULL,
	FOREIGN KEY ("owner_ID") REFERENCES "gtoverseer"."user"("ID") ON DELETE SET NULL
);

CREATE TABLE "gtoverseer"."work" (
	"ID"					SERIAL PRIMARY KEY,
	"machine_ID"			INT NOT NULL UNIQUE,
	"work_progress"			INT NOT NULL DEFAULT 0,
	"work_progress_max"		INT NOT NULL DEFAULT 0,
	"last_worked_at"		TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

	FOREIGN KEY ("machine_ID") REFERENCES "gtoverseer"."machine"("ID") ON DELETE CASCADE
);

CREATE TABLE "gtoverseer"."coord" (
	"ID"				SERIAL PRIMARY KEY,
	"machine_ID" 		INT NOT NULL UNIQUE,
	"x"					INT NOT NULL,
	"y" 				INT NOT NULL,
	"z" 				INT NOT NULL,
	"DIM" 				INT,
	"is_chunk_loaded"	BOOLEAN NOT NULL DEFAULT FALSE,

	FOREIGN KEY ("machine_ID") REFERENCES "gtoverseer"."machine"("ID") ON DELETE CASCADE
);

CREATE TABLE "gtoverseer"."power_source" (
	"ID"					SERIAL PRIMARY KEY,
	"machine_ID"			INT	NOT NULL UNIQUE,
	"output_amp"			INT NOT NULL,
	"current_capacity"		BIGINT NOT NULL,
	"max_capacity"			BIGINT NOT NULL,

	FOREIGN KEY ("machine_ID") REFERENCES "gtoverseer"."machine"("ID") ON DELETE CASCADE
);

CREATE TABLE "gtoverseer"."power_network_power_source" (
	"power_network_ID"		INT NOT NULL,
	"power_source_ID"		INT NOT NULL,
	"is_stable"				BOOLEAN NOT NULL DEFAULT TRUE,

	FOREIGN KEY ("power_network_ID") REFERENCES "gtoverseer"."power_network"("ID") ON DELETE CASCADE,
	FOREIGN KEY ("power_source_ID") REFERENCES "gtoverseer"."power_source"("ID") ON DELETE CASCADE
);

CREATE TABLE "gtoverseer"."machine_maintenance" (
	"ID"				SERIAL PRIMARY KEY,
	"machine_ID"		INT NOT NULL,
	"maintenance_ID" 	INT NOT NULL,
	"failure_at"		TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
	"repaired_at"		TIMESTAMP,
	"is_fixed"			BOOLEAN NOT NULL DEFAULT FALSE,

	FOREIGN KEY ("machine_ID") REFERENCES "gtoverseer"."machine"("ID") ON DELETE CASCADE,
	FOREIGN KEY ("maintenance_ID") REFERENCES "gtoverseer"."maintenance"("ID") ON DELETE CASCADE
);

--------- DML ---------
INSERT INTO "gtoverseer"."tier" ("name", "eu") VALUES -- STATIC
	('ULV', 8),
	('LV', 32),
	('MV', 128),
	('HV', 512),
	('EV', 2048),
	('IV', 8192),
	('LuV', 32768),
	('ZPM', 131072),
	('UV', 524288),
	('UHV', 2097152),
	('UEV', 8388608),
	('UIV', 33554432),
	('UMV', 134217728),
	('UXV', 536870912);

INSERT INTO "gtoverseer"."maintenance" ("message", "tool") VALUES -- STATIC
	('Pipe is loose.', 'Wrench'),
	('Screws are loose.', 'Screwdriver'),
	('Something is stuck.', 'Soft Mallet'),
	('Platings are dented.', 'Hammer'),
	('Circuitry burned out.', 'Soldering Iron'),
	('That doesn''t belong there.', 'Crowbar');

-- example priveleges (prob. shuld make some defaults)
INSERT INTO "gtoverseer"."privilege" ("name") VALUES
	('View Machine Status'),
	('Control Machine'),
	('Manage Machine'),
	('View Network Status'),
	('Manage Network'),
	('Manage Users'),
	('View Maintenance'),
	('Manage Maintenance'),
	('View Logs'),
	('Manage Logs');

-- example users
INSERT INTO "gtoverseer"."user" ("nickname", "email", "password_hash") VALUES
	('Meemlus', 'meemlus@email.cz', 'heslicko'),
	('_Zyosh_', 'zyosh@email.cz', 'maslicko'),
	('bobik', 'bobik@email.cz', 'jahoda'),
	('pepik', 'jahodak@email.cz', 'svickova'),
	('rostik', 'rostik@email.cz', 'smazak'),
	('kolik', 'maverick@email.cz', 'spaneslky ptacek'),
	('igor', 'igor@email.cz', 'spagety');

-- some example cables
INSERT INTO "gtoverseer"."cable" ("name", "density", "tier_ID", "max_amp", "loss") VALUES
	('Red Alloy Cable', '1', (SELECT "ID" FROM "gtoverseer"."tier" WHERE "name" = 'ULV'), '1', '0'),
	('Lead Cable', '1',  (SELECT "ID" FROM "gtoverseer"."tier" WHERE "name" = 'LV'), '2', '2'),
	('Tin Cable', '1',  (SELECT "ID" FROM "gtoverseer"."tier" WHERE "name" = 'LV'), '1', '1'),
	('Annealed Copper Cable', '4',  (SELECT "ID" FROM "gtoverseer"."tier" WHERE "name" = 'MV'), '4', '1'),
	('Gold Cable', '16',  (SELECT "ID" FROM "gtoverseer"."tier" WHERE "name" = 'HV'), '48', '2'),
	('Blue Alloy Cable', '1',  (SELECT "ID" FROM "gtoverseer"."tier" WHERE "name" = 'HV'), '2', '1'),
	('Aluminium Cable', '16',  (SELECT "ID" FROM "gtoverseer"."tier" WHERE "name" = 'EV'), '16', '1'),
	('TPV-Alloy Cable', '12',  (SELECT "ID" FROM "gtoverseer"."tier" WHERE "name" = 'EV'), '72', '1'),
	('Platinum Cable', '16',  (SELECT "ID" FROM "gtoverseer"."tier" WHERE "name" = 'IV'), '32', '1'),
	('Niobium-Titanium Cable', '1',  (SELECT "ID" FROM "gtoverseer"."tier" WHERE "name" = 'LuV'), '4', '2');

-- example power_networks
INSERT INTO "gtoverseer"."power_network" ("name", "cable_ID", "avg_amp", "avg_eu", "owner_ID") VALUES
	('bees', (SELECT "ID" FROM "gtoverseer"."cable" WHERE "name" = 'Gold Cable' AND "density" = '16'), NULL, NULL, (SELECT "ID" FROM "gtoverseer"."user" WHERE "nickname" = 'Meemlus')),
	('nuclear subnet', (SELECT "ID" FROM "gtoverseer"."cable" WHERE "name" = 'TPV-Alloy Cable' AND "density" = '12'), 38.7, 79257.6, (SELECT "ID" FROM "gtoverseer"."user" WHERE "nickname" = 'bobik')),
	('main north', (SELECT "ID" FROM "gtoverseer"."cable" WHERE "name" = 'Platinum Cable' AND "density" = '16'), NULL, NULL, (SELECT "ID" FROM "gtoverseer"."user" WHERE "nickname" = 'bobik')),
	('main east', (SELECT "ID" FROM "gtoverseer"."cable" WHERE "name" = 'TPV-Alloy Cable' AND "density" = '12'), NULL, NULL, (SELECT "ID" FROM "gtoverseer"."user" WHERE "nickname" = 'bobik')),
	('main south', (SELECT "ID" FROM "gtoverseer"."cable" WHERE "name" = 'Platinum Cable' AND "density" = '16'), NULL, NULL, (SELECT "ID" FROM "gtoverseer"."user" WHERE "nickname" = 'bobik')),
	('main west', (SELECT "ID" FROM "gtoverseer"."cable" WHERE "name" = 'TPV-Alloy Cable' AND "density" = '12'), NULL, NULL, (SELECT "ID" FROM "gtoverseer"."user" WHERE "nickname" = 'igor'));


------- VIEWS -----------
CREATE OR REPLACE VIEW "gtoverseer"."machine_report" AS
SELECT 
m."ID" AS machine_id,
m."name" AS machine_name,
m."oc_address" AS oc_address,
m."amp" AS machine_amp,
m."created_at" AS machine_created_at,
c."x" AS coord_x,
c."y" AS coord_y,
c."z" AS coord_z,
c."is_chunk_loaded" AS is_chunk_loaded,
case
	WHEN  w."work_progress_max" = 0 then 0
	else ((w."work_progress"::FLOAT / w."work_progress_max") * 100)
end AS "work_progress",
COALESCE(mm."is_fixed",TRUE) AS is_operational,
pn."name" AS power_network_name
FROM "gtoverseer"."machine" m
LEFT JOIN "gtoverseer"."coord" c ON m."ID" = c."machine_ID"
LEFT JOIN "gtoverseer"."work" w ON m."ID" = w."machine_ID"
LEFT JOIN "gtoverseer"."machine_maintenance" mm ON m."ID" = mm."machine_ID"
LEFT JOIN "gtoverseer"."power_network" pn ON m."power_network_ID" = pn."ID"
WHERE m."is_connected" = TRUE;

------- PRIVILEGES -----------
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
DROP SCHEMA IF EXISTS public CASCADE;

CREATE ROLE gtoverseer_app WITH LOGIN ENCRYPTED PASSWORD '${GTOVERSEER_POSTGRES_PASSWORD}';

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


