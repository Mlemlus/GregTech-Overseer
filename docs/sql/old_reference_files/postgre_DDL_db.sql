DROP SCHEMA IF EXISTS "db" CASCADE;
CREATE SCHEMA "db";

CREATE TABLE "db"."oc_computer" (
    "ID"			SERIAL PRIMARY KEY,
    "oc_address"	CHAR(32) NOT NULL UNIQUE
);

CREATE TABLE "db"."tier" (
    "ID"		SERIAL	PRIMARY KEY,
    "name" 		VARCHAR(3) NOT NULL,
    "eu" 		INT NOT NULL
);
    
CREATE TABLE "db"."maintenance" (
    "ID"		SERIAL PRIMARY KEY,
    "message" 	VARCHAR(30) NOT NULL,
    "tool"		VARCHAR(20) NOT NULL
);

CREATE TABLE "db"."control" (
	"ID"			SERIAL PRIMARY KEY,
    "name"			VARCHAR(30) NOT NULL,
	"is_manual"		BOOLEAN NOT NULL DEFAULT FALSE
);
 
CREATE TABLE "db"."privilege" (
	"ID"		SERIAL PRIMARY KEY,
    "name"		VARCHAR(30) NOT NULL
);

CREATE TABLE "db"."user" (
	"ID"				SERIAL PRIMARY KEY,
	"username"			VARCHAR(50) NOT NULL UNIQUE,
    "username"			VARCHAR(100),
    "password_hash"		CHAR(64)
);

CREATE TABLE  "db"."log" (
	"ID"		SERIAL PRIMARY KEY,
	"time"		TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "text"		VARCHAR(255) NOT NULL,
    "user_ID"	INT,
    
	FOREIGN KEY ("user_ID") REFERENCES "db"."user"("ID")
);
 
 CREATE TABLE "db"."cable" (
    "ID"		SERIAL PRIMARY KEY,
	"name"		VARCHAR(50) NOT NULL,
    "density"	SMALLINT NOT NULL,
    "tier_ID"	INT NOT NULL,
    "max_amp"	INT NOT NULL,
    "loss"		SMALLINT NOT NULL,
    
    FOREIGN KEY ("tier_ID") REFERENCES "db"."tier"("ID")
);
 
 CREATE TABLE "db"."power_network" (
    "ID"				SERIAL PRIMARY KEY,
	"name"				VARCHAR(100) NOT NULL UNIQUE,
    "cable_ID"			INT NOT NULL,
    "avg_amp"			DECIMAL(12,2),
    "avg_eu"			DECIMAL(22,2),
    "created_by_ID"		INT,
    "created_at"		DATE DEFAULT CURRENT_DATE NOT NULL,
	
    FOREIGN KEY ("cable_ID") REFERENCES "db"."cable"("ID") ON DELETE CASCADE,
    FOREIGN KEY ("created_by_ID") REFERENCES "db"."user"("ID")
);

CREATE TABLE "db"."user_privilege" (
	"user_ID"			INT NOT NULL,
    "privilege_ID"		INT NOT NULL,
    "is_shareable"		BOOLEAN NOT NULL DEFAULT FALSE,
    
    FOREIGN KEY ("user_ID") REFERENCES "db"."user"("ID"),
    FOREIGN KEY ("privilege_ID") REFERENCES "db"."privilege"("ID")
);

CREATE TABLE "db"."machine" (
	"ID"					SERIAL PRIMARY KEY,
    "oc_computer_ID" 		INT NOT NULL,
    "tier_ID"				INT NOT NULL,
    "power_network_ID"		INT,
    "owner_ID"				INT,
	"oc_address" 			CHAR(32) NOT NULL,
    "name"					VARCHAR(100) NOT NULL,
    "custom_name" 			VARCHAR(100),
    "amp"					SMALLINT NOT NULL,
    "created_at"			TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "note"					TEXT,
	"is_connected"			BOOLEAN NOT NULL DEFAULT TRUE,
    
	FOREIGN KEY ("oc_computer_ID") REFERENCES "db"."oc_computer"("ID") ON DELETE NO ACTION,
	FOREIGN KEY ("tier_ID") REFERENCES "db"."tier"("ID"),
	FOREIGN KEY ("power_network_ID") REFERENCES "db"."power_network"("ID") ON DELETE SET NULL,
	FOREIGN KEY ("owner_ID") REFERENCES "db"."user"("ID") ON DELETE SET NULL
);

CREATE TABLE "db"."work" (
    "ID"                    SERIAL PRIMARY KEY,
    "machine_ID"            INT NOT NULL UNIQUE,
    "work_progress"			INT NOT NULL DEFAULT 0,
    "work_progress_max"		INT NOT NULL DEFAULT 0,
    "last_worked_at"		TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, -- trigger update

    FOREIGN KEY ("machine_ID") REFERENCES "db"."machine"("ID") ON DELETE CASCADE
);

CREATE TABLE "db"."coord" (
    "ID"				SERIAL PRIMARY KEY,
    "machine_ID" 		INT NOT NULL UNIQUE,
    "x"					INT NOT NULL,
    "y" 				INT NOT NULL,
    "z" 				INT NOT NULL,
	"DIM" 				INT,
    "is_chunk_loaded"	BOOLEAN NOT NULL DEFAULT FALSE,
    
    FOREIGN KEY ("machine_ID") REFERENCES "db"."machine"("ID") ON DELETE CASCADE
);

CREATE TABLE "db"."machine_maintenance" (
    "ID"				SERIAL PRIMARY KEY,
    "machine_ID"		INT NOT NULL,
    "maintenance_ID" 	INT NOT NULL,
    "failure_at"		TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
	"repair_at"		    TIMESTAMP,
    "is_fixed"			BOOLEAN NOT NULL DEFAULT FALSE,
    
    FOREIGN KEY ("machine_ID") REFERENCES "db"."machine"("ID") ON DELETE CASCADE,
    FOREIGN KEY ("maintenance_ID") REFERENCES "db"."maintenance"("ID")
);

CREATE TABLE "db"."power_source" (
    "ID"					SERIAL	PRIMARY KEY,
	"machine_ID"			INT	NOT NULL,
    "output_amp"			INT NOT NULL,
    "current_capacity"		INT NOT NULL,
    "max_capacity"			INT NOT NULL,
    
    FOREIGN KEY ("machine_ID") REFERENCES "db"."machine"("ID") ON DELETE CASCADE
);

CREATE TABLE "db"."power_network_power_source" (
	"power_network_ID"		INT NOT NULL,
    "power_source_ID"		INT NOT NULL,
    "is_stable"				BOOLEAN DEFAULT TRUE,
    
    FOREIGN KEY ("power_network_ID") REFERENCES "db"."power_network"("ID") ON DELETE CASCADE,
    FOREIGN KEY ("power_source_ID") REFERENCES "db"."power_source"("ID") ON DELETE CASCADE
);

CREATE TABLE "db"."machine_control" (
	"machine_ID"		INT NOT NULL,
    "control_ID"		INT NOT NULL,
    "user_ID"			INT,
    "configured_at"		TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    
	FOREIGN KEY ("machine_ID") REFERENCES "db"."machine"("ID") ON DELETE CASCADE,
    FOREIGN KEY ("control_ID") REFERENCES "db"."control"("ID"),
	FOREIGN KEY ("user_ID") REFERENCES "db"."user"("ID")
);

