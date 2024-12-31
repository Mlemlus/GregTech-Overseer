-- 1. Create a query that retrieves only selected columns from the specified table.
SELECT "name", "density", "max_amp" as "max amp" FROM gtoverseer.cable

-- 2. Create a query that selects a user/person or a similar table based on the email.
SELECT * from gtoverseer.user WHERE "email" = 'jahodak@email.cz'

-- 3. Develop at least one UPDATE, INSERT, DELETE, and ALTER TABLE query.
UPDATE gtoverseer.work SET "work_progress" = 0 WHERE "ID" BETWEEN 50 AND 60;
SELECT * FROM gtoverseer.work

DELETE FROM gtoverseer.privilege WHERE "name" = 'non-privileged'
INSERT INTO gtoverseer.privilege ("name") VALUES ('non-privileged');
ALTER TABLE gtoverseer.privilege ADD "temp" VARCHAR(2);
ALTER TABLE gtoverseer.privilege DROP COLUMN "temp";
SELECT * FROM gtoverseer.privilege

-- 4.
-- (a) WHERE; WHERE with AND; WHERE with OR; WHERE with BETWEEN
SELECT * from gtoverseer.user WHERE "email" = 'jahodak@email.cz'
SELECT * from gtoverseer.machine WHERE "name" = 'basicmachine.assembler.tier.04' AND  "is_connected" = 'true'
SELECT * from gtoverseer.machine WHERE "name" = 'basicmachine.assembler.tier.04' OR  "name" = 'multimachine.blastfurnace'
SELECT * from gtoverseer.work WHERE "work_progress" BETWEEN 0 AND 200

-- (b) LIKE; NOT LIKE
SELECT * from gtoverseer.user WHERE "email" LIKE '%mail.cz'
SELECT * FROM gtoverseer.privilege WHERE "name" NOT LIKE '%Machine%'

-- (c) SUBSTRING; TRIM; CONCAT; COALESCE
SELECT SUBSTRING("name" FROM POSITION('.' IN "name") + 1) AS "multimachine type" 
	FROM gtoverseer.machine WHERE "name" LIKE 'multimachine%';
SELECT TRIM('     nejaky text  ') AS "string"  -- doslova vsechny hodnoty jsou perfektni
SELECT CONCAT(time,': ', text) AS "log" FROM gtoverseer.log
SELECT m.name, COALESCE(u."username", 'No owner') AS "owner" FROM gtoverseer.machine m 
	LEFT JOIN gtoverseer.user u ON m."owner_ID" = u."ID"

-- (d) SUM; MIN; MAX; AVG;
SELECT SUM(current_capacity) AS "Total EU Capacity" from gtoverseer.power_source
SELECT MIN(work_progress_max) AS "Lazy machine work" FROM gtoverseer.work
SELECT MAX(work_progress_max) AS "Hard working machine work" FROM gtoverseer.work
SELECT AVG(max_capacity) AS "Average EU capacity of power sources" FROM gtoverseer.power_source

-- (e) GROUP BY; GROUP BY and HAVING; GROUP BY, HAVING, and WHERE;
-- GROUP BY;
SELECT "oc_computer_ID", COUNT(*) AS "Number of machines under controller" 
FROM gtoverseer.machine 
GROUP BY "oc_computer_ID"
-- GROUP BY and HAVING;
SELECT "oc_computer_ID", COUNT(*) AS "Number of basic machines under controller"
FROM gtoverseer.machine
GROUP BY "oc_computer_ID"
HAVING COUNT("ID") > 11
-- GROUP BY, HAVING, and WHERE;
SELECT "oc_computer_ID", COUNT(*) AS "Number of basic machines under controller"
FROM gtoverseer.machine
WHERE "name" LIKE 'basic%'
GROUP BY "oc_computer_ID"
HAVING COUNT("ID") > 11

-- (f) UNION ALL / UNION; DISTINCT; COUNT; EXCEPT; INTERSECT
CREATE TABLE "gtoverseer"."new_tier" ( -- tmp table
    "ID"		SERIAL	PRIMARY KEY,
	"new_name" 	VARCHAR(3) NOT NULL,
    "eu" 		INT NOT NULL
);
INSERT INTO "gtoverseer"."new_tier" ("new_name", "eu") VALUES 
	('UXL', 2),
	('MLV', 16),
	('LV', 32),
	('MV', 128),
	('HV', 512),
	('EV', 2048);
SELECT * FROM gtoverseer.new_tier;
SELECT * FROM gtoverseer.tier;

-- UNION ALL / UNION;
SELECT "name","eu" FROM gtoverseer.tier
UNION
SELECT "new_name", "eu" FROM gtoverseer.new_tier
ORDER BY "eu"
-- DISTINCT;
SELECT DISTINCT "name" FROM gtoverseer.machine
-- COUNT;
SELECT COUNT(*) as "number of machines" FROM gtoverseer.machine
-- EXCEPT;
SELECT "name", "eu" FROM gtoverseer.tier
EXCEPT
SELECT "new_name", "eu" FROM gtoverseer.new_tier
ORDER BY "eu"
-- INTERSECT
SELECT "name", "eu" FROM gtoverseer.tier
INTERSECT
SELECT "new_name", "eu" FROM gtoverseer.new_tier
ORDER BY "eu"

DROP TABLE gtoverseer.new_tier -- clear

-- (g) LEFT JOIN; RIGHT JOIN; FULL OUTER JOIN; NATURAL JOIN
-- LEFT JOIN;
SELECT m.name, ps.output_amp FROM gtoverseer.power_source ps
LEFT JOIN gtoverseer.machine m ON ps."machine_ID" = m."ID"
--RIGHT JOIN;
SELECT m.name, ps.output_amp FROM gtoverseer.power_source ps
RIGHT JOIN gtoverseer.machine m ON ps."machine_ID" = m."ID"
-- FULL OUTER JOIN;
SELECT m.name, u.username FROM gtoverseer.machine m
FULL OUTER JOIN gtoverseer.user u ON m."owner_ID" = u."ID"
-- NATURAL JOIN
ALTER TABLE gtoverseer.machine RENAME COLUMN "ID" TO "machine_ID"
SELECT * FROM gtoverseer.machine
NATURAL JOIN gtoverseer.power_source
ALTER TABLE gtoverseer.machine RENAME COLUMN "machine_ID" TO "ID"

-- 7. Utilize in one query: LEFT JOIN, GROUP BY, HAVING, ORDER BY, AVG, and DISTINCT.
-- avg max machine work by tier
SELECT DISTINCT t."name" AS "Tier", AVG(w.work_progress_max) as "Avg max progress"
FROM gtoverseer.machine m
LEFT JOIN gtoverseer.work w ON m."ID" = w."machine_ID"
LEFT JOIN gtoverseer.tier t ON m."tier_ID" = t."ID"
GROUP BY t."name"
HAVING AVG(w.work_progress_max) > 0
ORDER BY "Avg max progress" DESC

-- 8. Create a query that employs any aggregate function and utilizes GROUP BY with HAVING.
SELECT m."name", SUM(w.work_progress_max) AS "Sum max progress"
FROM gtoverseer.machine m
LEFT JOIN gtoverseer.work w ON m."ID" = w."machine_ID"
GROUP BY m."name"
HAVING SUM(w.work_progress_max) > 1000
ORDER BY "Sum max progress" DESC;

-- 9. Formulate a query that joins at least three tables and uses GROUP BY, COUNT, and HAVING.
SELECT oc."oc_address" AS "Controller address", t."name" AS "Tier", COUNT(m."ID") AS "Number of machines under controller" 
FROM gtoverseer.machine m
LEFT JOIN gtoverseer.oc_computer oc ON m."oc_computer_ID" = oc."ID"
LEFT JOIN gtoverseer.tier t ON m."tier_ID" = t."ID"
GROUP BY oc."oc_address", t."name"
HAVING COUNT(m."ID") > 7

-- 10. Develop a query that retrieves data from an arbitrary table for the last one and a half days 
-- (1 day + 12 hours, i.e., 36 hours). Avoid hard-coding the query (e.g., created at > 7-11-2021)!
--		(a) Do it programmatically with DATE functions.
CREATE TABLE	"gtoverseer"."fake_log" (
	"ID"		SERIAL PRIMARY KEY,
	"time"		TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "text"		VARCHAR(255) NOT NULL   
);
INSERT INTO "gtoverseer"."fake_log" ("text", "time") VALUES
	('0. Test system inicialization', current_timestamp - (2 * interval '1 month')),
	('Connecting to OC...', current_timestamp - (2 * interval '1 month')),
	('Failed!', current_timestamp - (2 * interval '1 month')),
	('1. System inicialization', current_timestamp - (40 * interval '1 day')),
	('Connecting to OC...', current_timestamp - (40 * interval '1 day')),
	('Failed!', current_timestamp - (40 * interval '1 day')),
	('Retrying connection...', current_timestamp - (40 * interval '1 day')),
	('Logged in', current_timestamp - (40 * interval '1 day')),
	('2. System inicialization', current_timestamp - (40 * interval '1 hour')),
	('Connecting to OC...', current_timestamp - (40 * interval '1 hour')),
	('Failed!', current_timestamp - (40 * interval '1 hour')),
	('Retrying connection...', current_timestamp - (40 * interval '1 hour')),
	('Logged in', current_timestamp - (40 * interval '1 hour')),
	('3. System inicialization', current_timestamp),
	('Connecting to OC...', current_timestamp),
	('Failed!', current_timestamp),
	('Retrying connection...', current_timestamp),
	('Logged in', current_timestamp);
select * from gtoverseer.fake_log;

-- retrieves data from last (1 day + 12 hours, i.e., 36 hours)
SELECT *
FROM gtoverseer.fake_log
WHERE "time" >= current_timestamp - (36 * interval '1 hour')
ORDER BY "time" DESC;
	
-- 11. Create a query that returns data from the last month (starting from the first day of the month).
SELECT * FROM gtoverseer.fake_log
WHERE "time" >= date_trunc('month', CURRENT_DATE) - INTERVAL '1 month' AND "time" < date_trunc('month', CURRENT_DATE)
ORDER BY "time" DESC;

DROP TABLE gtoverseer.fake_log -- clear

-- Create a SELECT statement that removes accents from a selected string (e.g., á will be converted to a).
UPDATE gtoverseer.machine SET "note" = 'Ačkoliv nemám rád všechna ta přirovnání a podobenství, kterými doktor Vlach proplétá své temperamentní řeči, uznávám, že na tom názorném příkladu s kavárnou, člověkem a mísou koblih něco je. Lze na něm aspoň přibližně ukázat, jakým člověkem je Saturnin. Doktor Vlach si totiž rozdělil lidi podle toho, jak se chovají v poloprázdné kavárně, mají-li před sebou mísu koblih. Představte si luxusní kavárnu za nedělního odpoledne. Venku je krásný den a hostů v kavárně je málo. Už jste se nasnídali, přečetli jste všechny noviny a teď jste se pohodlně opřeli v měkkém boxu a zamyšleně se díváte na mísu koblih. Nuda se pomalu rozlézá do všech koutů kavárny.' WHERE "ID" = 40
UPDATE gtoverseer.machine SET "note" = 'Myslím, že jsem se už zmínil, že mám tetu jménem Kateřina. Neštěstí nechodí po horách, ale po lidech. Teta Kateřina má syna. Je mu 18 let a jmenuje se Milouš. Neštěstí nechodí nikdy samo. Teta Kateřina je vdova a Milouš je sirotek, protože strýc František před deseti lety zemřel. Jistě nelituje, že to udělal. Poslouchat celý život přísloví, pořekadla a zrnka moudrosti není maličkost.' WHERE "ID" = 41
SELECT * FROM
	(SELECT "ID", gtoverseer.unaccent("note") AS "note" FROM gtoverseer.machine
	WHERE "note" IS NOT NULL) 
UNION ALL
	(SELECT "ID", "note" FROM gtoverseer.machine
	WHERE "note" IS NOT NULL)
ORDER BY "ID" ASC

-- 13. Create a query for pagination in an application (utilize LIMIT and OFFSET).
SELECT m."name", ((w."work_progress"::FLOAT / w."work_progress_max") * 100) AS "progress",w."work_progress", w."work_progress_max"  
FROM gtoverseer.machine m
LEFT JOIN gtoverseer.work w ON m."ID" = w."machine_ID"
ORDER BY w."work_progress_max" DESC
LIMIT 5 OFFSET 5; -- "2" stranka

-- 14. Formulate a query that uses a subquery in the FROM clause.
SELECT sq."name", sq."progress"
FROM(
	SELECT m."name", ((w."work_progress"::FLOAT / w."work_progress_max") * 100) AS "progress",w."work_progress", w."work_progress_max"
	FROM gtoverseer.machine m
	LEFT JOIN gtoverseer.work w ON m."ID" = w."machine_ID"
	ORDER BY w."work_progress_max" DESC
	LIMIT 10
)AS sq
WHERE sq."progress" > 10

-- 15. Develop a query that employs a subquery in the WHERE condition.
SELECT m."name", ((w."work_progress"::FLOAT / w."work_progress_max") * 100) AS "progress",w."work_progress", w."work_progress_max"  
FROM gtoverseer.machine m
LEFT JOIN gtoverseer.work w ON m."ID" = w."machine_ID"
WHERE w."work_progress_max" > (
	SELECT AVG("work_progress_max") 
	FROM gtoverseer.work)
ORDER BY w."work_progress_max" DESC

-- 16. Create a query that joins at least five tables.
SELECT 
m."name" AS "machine name", 
t."name" AS "tier",
((w."work_progress"::FLOAT / w."work_progress_max") * 100) AS "progress",
COALESCE(ps.output_amp, 0) AS "output amp",
oc."oc_address" AS "controller address",
u."username" AS "owner"
FROM gtoverseer.machine m
LEFT JOIN gtoverseer.coord c ON m."ID" = c."machine_ID"
LEFT JOIN gtoverseer.work w ON m."ID" = w."machine_ID"
LEFT JOIN gtoverseer.power_source ps ON m."ID" = ps."machine_ID"
LEFT JOIN gtoverseer.oc_computer oc ON m."oc_computer_ID" = oc."ID"
LEFT JOIN gtoverseer.tier t ON m."tier_ID" = t."ID"
LEFT JOIN gtoverseer.user u ON m."owner_ID" = u."ID"
ORDER BY "machine name"

-- 18. Create database indexes only on columns where it makes sense.
-- 	Before creating a database index, execute a query using the WHERE condition on a column without an index. 
-- 	Then, perform the same query on the column with an index.

--CREATE INDEX IF NOT EXISTS idx_machine_name ON "gtoverseer"."machine"("name");
--CREATE INDEX IF NOT EXISTS idx_machine_custom_name ON "gtoverseer"."machine"("custom_name");
EXPLAIN SELECT * FROM gtoverseer.machine
WHERE "name" = 'multimachine.vacuumfreezer' 

-- 19. Create an arbitrary database procedure (consider a suitable case).
CREATE OR REPLACE PROCEDURE gtoverseer.del_disconnected_machines(days INT)
AS $$
BEGIN
	DELETE FROM gtoverseer.machine m
	USING gtoverseer.work w
	WHERE m."ID" = w."machine_ID" AND w."last_worked_at" < (NOW() - INTERVAL '1 day' * days);
END;
$$ LANGUAGE plpgsql;

SELECT * FROM gtoverseer.work WHERE "machine_ID" = 31
UPDATE gtoverseer.work SET "last_worked_at" = (NOW() - INTERVAL '50 day') WHERE "machine_ID" = 32
CALL gtoverseer.del_disconnected_machines(49)
SELECT * FROM gtoverseer.machine WHERE "ID" = 32

-- 20. Create an arbitrary database function (consider a suitable case).
CREATE OR REPLACE FUNCTION gtoverseer.get_total_eu_usage(network_ID INT)
RETURNS INTEGER AS $$
DECLARE total_eu INTEGER;
BEGIN 
    SELECT SUM(t."eu" * m."amp") INTO total_eu
    FROM gtoverseer.machine m
	JOIN gtoverseer.tier t ON m."tier_ID" = t."ID"
    WHERE m."power_network_ID" = network_id;
RETURN total_eu;
END;
$$ LANGUAGE plpgsql;

SELECT gtoverseer.get_total_eu_usage(2)

UPDATE gtoverseer.machine SET "power_network_ID" = 2 WHERE "ID" BETWEEN 30 AND 55
SELECT * FROM gtoverseer.machine

-- 21. Create arbitrary database trigger.
CREATE OR REPLACE FUNCTION gtoverseer.upd_last_worked_at()
RETURNS TRIGGER AS $$
BEGIN
	UPDATE "gtoverseer"."work" SET "last_worked_at" = NOW() 
	WHERE "ID" = NEW."ID";
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER update_last_worked_at
AFTER UPDATE ON "gtoverseer"."work"
FOR EACH ROW 
WHEN (OLD."work_progress" IS DISTINCT FROM NEW."work_progress")
EXECUTE FUNCTION gtoverseer.upd_last_worked_at();

SELECT * FROM gtoverseer.work WHERE "ID" = 36
UPDATE gtoverseer.work SET "work_progress" = 450 WHERE "ID" = 36

-- 22. Create arbitrary database view (consider some complex cases).
DROP VIEW "gtoverseer"."machine_report"
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
((w."work_progress"::FLOAT / w."work_progress_max") * 100) AS "work_progress",
COALESCE(mm."is_fixed",TRUE) AS is_operational,
pn."name" AS power_network_name
FROM "gtoverseer"."machine" m
LEFT JOIN "gtoverseer"."coord" c ON m."ID" = c."machine_ID"
LEFT JOIN "gtoverseer"."work" w ON m."ID" = w."machine_ID"
LEFT JOIN "gtoverseer"."machine_maintenance" mm ON m."ID" = mm."machine_ID"
LEFT JOIN "gtoverseer"."power_network" pn ON m."power_network_ID" = pn."ID"
WHERE m."is_connected" = TRUE;

SELECT * FROM gtoverseer.machine_report

-- 23. Create a database materialized view (consider a complex SQL query with several joins, 
-- aggregate functions, GROUP BY with HAVING, and a complex WHERE condition).
CREATE MATERIALIZED VIEW gtoverseer.power_network_report AS
SELECT
pn."ID" AS power_network_id,
pn."name" AS power_network_name,
COUNT(m."ID") AS machines,
COUNT(CASE WHEN w."work_progress" > 0 THEN m."ID" END) AS working_machines,
MAX(tc."eu" * c."max_amp") AS max_eu_allowed,
SUM(tm."eu" * m."amp") AS max_eu_usage,
SUM(CASE WHEN w."work_progress" > 0 THEN (tm."eu" * m."amp") END) AS current_eu_usage
FROM gtoverseer.power_network pn
LEFT JOIN gtoverseer.machine m ON m."power_network_ID" = pn."ID" 
LEFT JOIN gtoverseer.work w ON w."machine_ID" = m."ID"  
LEFT JOIN gtoverseer.tier tm ON m."tier_ID" = tm."ID"
LEFT JOIN gtoverseer.cable c ON pn."cable_ID" = c."ID"
LEFT JOIN gtoverseer.tier tc ON c."tier_ID" = tc."ID"
GROUP BY pn."ID", pn."name"
HAVING COUNT(m."ID") > 0
ORDER BY machines DESC;

SELECT * FROM gtoverseer.power_network_report
-- SELECT pn."name", SUM(t."eu" * m."amp") AS max_eu_usage
-- FROM gtoverseer.machine m
-- JOIN gtoverseer.power_network pn ON m."power_network_ID" = pn."ID"
-- LEFT JOIN gtoverseer.tier t ON m."tier_ID" = t."ID"
-- GROUP BY pn."name"

-- 24. If you are using the public schema, create a new schema for your database called bds.
CREATE SCHEMA bds; -- jenom pro projekt 2
--	(b) Revoke the CREATE privilege on the public schema from the public role.
REVOKE CREATE ON SCHEMA public FROM PUBLIC;

-- 25. Create two roles, bds-app and bds-script, in your database.
CREATE ROLE bds_app WITH LOGIN PASSWORD 'aplikejsn*';
CREATE ROLE bds_script WITH LOGIN PASSWORD 'skriptos*';
--	(a) Assign the bds-app role privileges to SELECT, INSERT, UPDATE, and DELETE everything in an arbitrary table in the bds schema. 
--	Additionally, configure bds-app to viewonly specific fields (e.g., excluding salary from the “person” or your “user” object).
CREATE TABLE bds.person (
	"ID" SERIAL PRIMARY KEY,
	"name" VARCHAR(100) NOT NULL,
	"email" VARCHAR(100),
	"salary" INT
);
INSERT INTO bds.person (name, email, salary)
VALUES
('Pepik', 'pepik@email.com', 50000),
('Bob', 'bob@email.com', 60000),
('Lenka', 'lenka@email.com', 70000);

GRANT SELECT, INSERT, UPDATE, DELETE ON "bds"."person" TO bds_app;
REVOKE SELECT (salary) ON bds.person FROM bds_app;
--	(b) Grant bds-app all privileges for all sequences in the bds schema.
GRANT USAGE ON SCHEMA bds TO bds_app;
GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA bds TO bds_app; -- sequence == serial aka ID
--	(c) Configure the privileges for bds-app so that the application can connect to the database using this user.
GRANT CONNECT ON DATABASE postgres TO bds_app;
--	(d) For bds-script, assign the ability to select only specific tables.
GRANT SELECT ON bds.person TO bds_script;

-- 26. Encrypt selected database columns (using pgcrypto module).
CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA "gtoverseer";
ALTER TABLE gtoverseer.user ADD email_enc BYTEA UNIQUE
ALTER TABLE gtoverseer.user ADD password_hash CHAR(60)

SELECT * FROM gtoverseer.user
UPDATE gtoverseer.user SET password = 'heslo'

UPDATE gtoverseer.user SET email_enc = gtoverseer.pgp_sym_encrypt(email, 'klicenka')

UPDATE gtoverseer.user SET "password_hash" = gtoverseer.crypt("password", gtoverseer.gen_salt('bf')) 

SELECT username, gtoverseer.pgp_sym_decrypt(email_enc, 'klicenka') AS email_dec
FROM gtoverseer.user 
WHERE password_hash = gtoverseer.crypt('heslo', password_hash)



