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

INSERT INTO "gtoverseer"."privilege" ("name") VALUES -- STATIC
	('Edit Machines'),
	('Remove Machines'),
	('Edit Power Source Machines'),
	('Add Power Networks'),
	('Edit Power Networks'),
	('Remove Power Networks'),
	('Add Cables'),
	('Edit Cables'),
	('View Logs'),
	('Manage Maintenance');