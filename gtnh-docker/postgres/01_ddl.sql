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
	"nickname"			VARCHAR(16) NOT NULL UNIQUE,
	"email"				VARCHAR UNIQUE,
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