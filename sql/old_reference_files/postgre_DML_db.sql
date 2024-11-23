INSERT INTO "db"."oc_computer" ("oc_address") VALUES
	('D35353FEC2CA425236A12C7A07DDE0DE'),
	('A720737B7EF1FF27BB41E9D0B60BD75C'),
	('183E0CE34DD450AED40A5EBF278597B4'),
	('CD971558A33524B4D2FCDBA091F60970'),
	('942D9605DFC3670CB8C5BF6031A140CB'),
	('F27F967F72DA50AB8C3D174D5EB6E854'),
	('B7C2D4C114BACF9DDAA18222AA02262D'),
	('18D8F29241668C38351B3CDBA02023B0'),
	('A37A74E22EA0C4A1CD4DAE9E4921F035'),
	('9A92100939E26C7CE15B27FCDECEF62E');
    
INSERT INTO "db"."tier" ("name", "eu") VALUES 
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

INSERT INTO "db"."maintenance" ("message", "tool") VALUES
	('Pipe is loose.', 'Wrench'),
	('Screws are loose.', 'Screwdriver'),
	('Something is stuck.', 'Soft Mallet'),
	('Platings are dented.', 'Hammer'),
	('Circuitry burned out.', 'Soldering Iron'),
	('That doesn''t belong there.', 'Crowbar');
    
INSERT INTO "db"."control" ("name", "is_manual") VALUES
	('Manual Machine Operation', '1'),
	('Automatic Production Mode', '0'),
	('Automatic Recipe Crafting Mode', '0'),
	('Remote Control', '1'),
	('Standalone Control', '1');
    
INSERT INTO "db"."privilege" ("name") VALUES
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

INSERT INTO "db"."user" ("nickname", "username", "password_hash") VALUES
	('bobik', NULL, NULL),
	('pepik', 'jahodak', '49d3a2d3bbefe54b1319a29252fb4d42dcef3c5a4413be06ff7ce7ee4c65ee3d'),
	('rostik', NULL, NULL),
	('kolik', 'maverick', 'b7d15b8e67fe009e2b26d5d2d63b3f2850fe3cc59e4ca114b2cc3bd5fcd9268d'),
	('igor', NULL, NULL);
    
INSERT INTO "db"."log" ("text", "user_ID") VALUES
	('System inicialization', NULL),
	('Connecting to OC...', NULL),
	('Failed!', NULL),
	('Retrying connection...', NULL),
	('Logged in', (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'pepik'));

INSERT INTO "db"."cable" ("name", "density", "tier_ID", "max_amp", "loss") VALUES
	('Red Alloy Cable', '1', (SELECT "ID" FROM "db"."tier" WHERE "name" = 'ULV'), '1', '0'),
	('Lead Cable', '1',  (SELECT "ID" FROM "db"."tier" WHERE "name" = 'LV'), '2', '2'),
	('Tin Cable', '1',  (SELECT "ID" FROM "db"."tier" WHERE "name" = 'LV'), '1', '1'),
	('Annealed Copper Cable', '4',  (SELECT "ID" FROM "db"."tier" WHERE "name" = 'MV'), '4', '1'),
	('Gold Cable', '16',  (SELECT "ID" FROM "db"."tier" WHERE "name" = 'HV'), '48', '2'),
	('Blue Alloy Cable', '1',  (SELECT "ID" FROM "db"."tier" WHERE "name" = 'HV'), '2', '1'),
	('Aluminium Cable', '16',  (SELECT "ID" FROM "db"."tier" WHERE "name" = 'EV'), '16', '1'),
	('TPV-Alloy Cable', '12',  (SELECT "ID" FROM "db"."tier" WHERE "name" = 'EV'), '72', '1'),
	('Platinum Cable', '16',  (SELECT "ID" FROM "db"."tier" WHERE "name" = 'IV'), '32', '1'),
	('Niobium-Titanium Cable', '1',  (SELECT "ID" FROM "db"."tier" WHERE "name" = 'LuV'), '4', '2');

INSERT INTO "db"."power_network" ("name", "cable_ID", "avg_amp", "avg_eu", "created_by_ID") VALUES
	('bees', (SELECT "ID" FROM "db"."cable" WHERE "name" = 'Gold Cable' AND "density" = '16'), NULL, NULL, NULL),
	('nuclear subnet', (SELECT "ID" FROM "db"."cable" WHERE "name" = 'TPV-Alloy Cable' AND "density" = '12'), 38.7, 79257.6, (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'bobik')),
	('main north', (SELECT "ID" FROM "db"."cable" WHERE "name" = 'Platinum Cable' AND "density" = '16'), NULL, NULL, NULL),
	('main east', (SELECT "ID" FROM "db"."cable" WHERE "name" = 'TPV-Alloy Cable' AND "density" = '12'), NULL, NULL, NULL),
	('main south', (SELECT "ID" FROM "db"."cable" WHERE "name" = 'Platinum Cable' AND "density" = '16'), NULL, NULL, NULL),
	('main west', (SELECT "ID" FROM "db"."cable" WHERE "name" = 'TPV-Alloy Cable' AND "density" = '12'), NULL, NULL, NULL);
    
INSERT INTO "db"."user_privilege" ("user_ID", "privilege_ID", "is_shareable") VALUES
	((SELECT "ID" FROM "db"."user" WHERE "nickname" = 'bobik'), (SELECT "ID" FROM "db"."privilege" WHERE "name" = 'View Machine Status'), '0'),
	((SELECT "ID" FROM "db"."user" WHERE "nickname" = 'bobik'), (SELECT "ID" FROM "db"."privilege" WHERE "name" = 'View Network Status'), '0'),
	((SELECT "ID" FROM "db"."user" WHERE "nickname" = 'bobik'), (SELECT "ID" FROM "db"."privilege" WHERE "name" = 'View Maintenance'), '1'),
	((SELECT "ID" FROM "db"."user" WHERE "nickname" = 'pepik'), (SELECT "ID" FROM "db"."privilege" WHERE "name" = 'View Machine Status'), '0'),
	((SELECT "ID" FROM "db"."user" WHERE "nickname" = 'pepik'), (SELECT "ID" FROM "db"."privilege" WHERE "name" = 'Control Machine'), '0'),
	((SELECT "ID" FROM "db"."user" WHERE "nickname" = 'pepik'), (SELECT "ID" FROM "db"."privilege" WHERE "name" = 'Manage Machine'), '0'),
	((SELECT "ID" FROM "db"."user" WHERE "nickname" = 'pepik'), (SELECT "ID" FROM "db"."privilege" WHERE "name" = 'View Network Status'), '0'),
	((SELECT "ID" FROM "db"."user" WHERE "nickname" = 'pepik'), (SELECT "ID" FROM "db"."privilege" WHERE "name" = 'Manage Network'), '0'),
	((SELECT "ID" FROM "db"."user" WHERE "nickname" = 'pepik'), (SELECT "ID" FROM "db"."privilege" WHERE "name" = 'Manage Users'), '1'),
	((SELECT "ID" FROM "db"."user" WHERE "nickname" = 'pepik'), (SELECT "ID" FROM "db"."privilege" WHERE "name" = 'View Maintenance'), '0'),
	((SELECT "ID" FROM "db"."user" WHERE "nickname" = 'pepik'), (SELECT "ID" FROM "db"."privilege" WHERE "name" = 'Manage Maintenance'), '0');

INSERT INTO "db"."machine" ("oc_computer_ID", "tier_ID", "power_network_ID", "owner_ID", "oc_address", "name", "custom_name", "amp", "work_progress", "work_progress_max", "note") VALUES
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = 'D35353FEC2CA425236A12C7A07DDE0DE'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'EV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'bees'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'bobik'), 'D66045A6A3466BA8776A23217FE6A8FA', 'multimachine.blastfurnace', 'uplne EBFko', '2', '3', '983', 'jakoze ebfkuje'),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = 'D35353FEC2CA425236A12C7A07DDE0DE'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'EV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'bees'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'bobik'), '9CA9A3ED5DFFD30A6738673C088556E7', 'multimachine.blastfurnace', NULL, '4', '0', '857', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = 'D35353FEC2CA425236A12C7A07DDE0DE'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'EV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'bees'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'bobik'), '0F3BED4175EC2E0D26C49339054C7F6B', 'multimachine.blastfurnace', NULL, '4', '0', '0', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = 'D35353FEC2CA425236A12C7A07DDE0DE'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'EV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'bees'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'bobik'), '0B7CC3E7D7A377FB8743C2BDFEC1EC6B', 'multimachine.blastfurnace', NULL, '2', '372', '881', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = 'D35353FEC2CA425236A12C7A07DDE0DE'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'EV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'bees'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'bobik'), '0C68D49A073668E07ACBB4C7932A5778', 'multimachine.blastfurnace', 'main upper', '1', '261', '840', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = 'D35353FEC2CA425236A12C7A07DDE0DE'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'EV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'bees'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'bobik'), '54411AC816F36DA974D561EECB9FF5E7', 'multimachine.blastfurnace', NULL, '1', '0', '0', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = 'D35353FEC2CA425236A12C7A07DDE0DE'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'EV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'bees'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'bobik'), 'D7AE5B89A2A93BB19BC907314D7108BF', 'multimachine.blastfurnace', NULL, '3', '142', '763', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = 'D35353FEC2CA425236A12C7A07DDE0DE'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'EV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'bees'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'bobik'), '421972C4D2AE0768682F227845F7B6CA', 'multimachine.blastfurnace', NULL, '2', '0', '0', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = 'D35353FEC2CA425236A12C7A07DDE0DE'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'EV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main north'), NULL, 'BDDE648F2E2D1D8443E9A87EA89A1012', 'multimachine.blastfurnace', NULL, '4', '169', '596', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = 'D35353FEC2CA425236A12C7A07DDE0DE'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'EV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main east'), NULL, 'AFF7C31170D5E07680FBA531101CADC6', 'multimachine.blastfurnace', 'NE QUAD', '1', '179', '937', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = 'A720737B7EF1FF27BB41E9D0B60BD75C'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'EV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main north'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'bobik'), 'BD8991493631948CDDC40DCCA5C5686E', 'multimachine.blastfurnace', 'NW QUAD', '2', '14', '949', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = 'A720737B7EF1FF27BB41E9D0B60BD75C'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'EV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main east'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'bobik'), 'FA4230FA683F36859D126192FC3098DA', 'multimachine.blastfurnace', 'SE QUAD', '2', '362', '558', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = 'A720737B7EF1FF27BB41E9D0B60BD75C'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'EV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main east'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'bobik'), 'B9F673C8069690CBA36CADB07C66301A', 'multimachine.blastfurnace', 'SW QUAD', '4', '235', '618', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = 'A720737B7EF1FF27BB41E9D0B60BD75C'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'EV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main east'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'pepik'), '2EC6000A3C7BEA1659D787CFE3A206F4', 'multimachine.blastfurnace', NULL, '2', '313', '754', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = 'A720737B7EF1FF27BB41E9D0B60BD75C'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'EV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main east'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'pepik'), '7BA3B38C2614D30E7B638BB7B2CE2DCC', 'multimachine.blastfurnace', NULL, '1', '245', '590', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = 'A720737B7EF1FF27BB41E9D0B60BD75C'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'IV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main east'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'pepik'), '8F843FA1E5C2466F69E28A3A778FE64B', 'basicgenerator.diesel.tier.03', NULL, '0', '0', '0', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = 'A720737B7EF1FF27BB41E9D0B60BD75C'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'IV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main east'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'pepik'), 'ED81F26E2785B426D91DF8166EB90864', 'basicgenerator.diesel.tier.03', NULL, '0', '0', '0', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = 'A720737B7EF1FF27BB41E9D0B60BD75C'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'IV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main east'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'pepik'), '6379EE0563C1C7BBAD7904BD0FCF7494', 'basicgenerator.diesel.tier.03', NULL, '0', '0', '0', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = 'A720737B7EF1FF27BB41E9D0B60BD75C'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'IV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main east'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'rostik'), '85EBFB1FE19B4D0E608EAB1FC5584BEC', 'basicgenerator.diesel.tier.03', NULL, '0', '0', '0', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = '183E0CE34DD450AED40A5EBF278597B4'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'IV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main east'), NULL, 'C68740708B6494AFCAF1ECDE9C4FA8AA', 'basicgenerator.diesel.tier.03', NULL, '0', '0', '0', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = '183E0CE34DD450AED40A5EBF278597B4'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'IV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main east'), NULL, '79F594F938579603E357C3D3DEF79D07', 'basicgenerator.diesel.tier.03', NULL, '0', '0', '0', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = '183E0CE34DD450AED40A5EBF278597B4'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'IV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main south'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'igor'), 'E991DE070F3BE74F8000BED02132F675', 'basicgenerator.diesel.tier.03', NULL, '0', '0', '0', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = '183E0CE34DD450AED40A5EBF278597B4'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'IV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main south'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'igor'), '09F18B74179D2DD3C51590F1B626CD4D', 'basicgenerator.diesel.tier.03', NULL, '0', '0', '0', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = '183E0CE34DD450AED40A5EBF278597B4'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'IV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main south'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'rostik'), '78BC7D4833801F8F31D0B574C6144914', 'multimachine.multifurnace', NULL, '2', '192', '625', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = '183E0CE34DD450AED40A5EBF278597B4'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'IV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main south'), NULL, '81273683B56C4822E1332BD95523A901', 'multimachine.multifurnace', NULL, '1', '418', '884', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = '183E0CE34DD450AED40A5EBF278597B4'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'IV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main south'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'igor'), 'EF95A5CF5DE0A38B7BE2BFE58CDC75B5', 'multimachine.multifurnace', NULL, '1', '271', '727', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = '183E0CE34DD450AED40A5EBF278597B4'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'IV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main north'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'igor'), 'E93CC56600B934F98A1F61ABBDD8AABD', 'multimachine.multifurnace', NULL, '3', '0', '0', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = '183E0CE34DD450AED40A5EBF278597B4'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'EV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main north'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'igor'), '0940D4070B32C0FB725C4EA6F7D5C401', 'multimachine.multifurnace', NULL, '1', '0', '0', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = '183E0CE34DD450AED40A5EBF278597B4'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'EV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main north'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'kolik'), '1B568F63D6156CF9EA5E251A6A8B297A', 'multimachine.multifurnace', NULL, '4', '286', '658', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = '183E0CE34DD450AED40A5EBF278597B4'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'EV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main north'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'igor'), '2B1CA797FCA846F163C796EF760C9E90', 'multimachine.multifurnace', NULL, '2', '425', '874', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = '942D9605DFC3670CB8C5BF6031A140CB'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'EV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main north'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'kolik'), '36C89F396BAFB062AF7B36C04942EEA8', 'multimachine.multifurnace', NULL, '4', '9', '556', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = '942D9605DFC3670CB8C5BF6031A140CB'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'EV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main north'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'kolik'), '7C075ACCF6E1608086DDEF5A65DB0E99', 'multimachine.multifurnace', NULL, '2', '415', '632', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = '942D9605DFC3670CB8C5BF6031A140CB'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'EV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main north'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'kolik'), 'C88CD4D8FF09EC47323BB7C27DB4DE94', 'multimachine.multifurnace', NULL, '1', '101', '553', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = '942D9605DFC3670CB8C5BF6031A140CB'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'EV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main north'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'kolik'), 'B82775282BBEEC348B3CB7EDDCBCC709', 'multimachine.multifurnace', NULL, '4', '95', '918', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = '942D9605DFC3670CB8C5BF6031A140CB'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'IV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main north'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'kolik'), '31CDB85FE69AD2673B5A3754A22CFF8F', 'basicmachine.distillery.tier.1', NULL, '1', '182', '511', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = '942D9605DFC3670CB8C5BF6031A140CB'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'IV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main south'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'kolik'), 'CEBA86B9EBA9672AEE245FE9E2E4C174', 'basicmachine.distillery.tier.2', NULL, '2', '484', '561', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = '942D9605DFC3670CB8C5BF6031A140CB'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'IV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main south'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'rostik'), 'AD2EA70F3504EC6CAAB0E3E46315FF7A', 'basicmachine.distillery.tier.3', NULL, '3', '0', '0', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = '942D9605DFC3670CB8C5BF6031A140CB'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'IV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main west'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'rostik'), '9B06C713C5113E9DCAA013B3EB7DE5FE', 'basicmachine.distillery.tier.4', NULL, '2', '318', '907', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = '942D9605DFC3670CB8C5BF6031A140CB'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'IV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main west'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'rostik'), '8FD16A538F0339003FFFD9F1F5C8E915', 'multimachine.chemicalreactor', NULL, '3', '9', '926', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = '942D9605DFC3670CB8C5BF6031A140CB'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'IV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main west'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'rostik'), 'DEABB2AF779A9525F1AB1C49EDDEA33A', 'multimachine.chemicalreactor', NULL, '1', '217', '544', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = '942D9605DFC3670CB8C5BF6031A140CB'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'IV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main west'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'rostik'), 'A908ACC6E21228ACD73C9BDBFDAC9F37', 'multimachine.chemicalreactor', NULL, '4', '207', '678', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = '18D8F29241668C38351B3CDBA02023B0'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'IV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main west'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'kolik'), 'A63868D0E1269DE815C14081E439DE22', 'multimachine.chemicalreactor', NULL, '2', '424', '788', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = '18D8F29241668C38351B3CDBA02023B0'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'IV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main west'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'kolik'), '3A1804C4C6D18EB69714337A2B524158', 'multimachine.chemicalreactor', NULL, '3', '372', '971', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = '18D8F29241668C38351B3CDBA02023B0'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'IV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main west'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'rostik'), 'EC2960B5EAB018786DB72C2DDC524EC0', 'multimachine.chemicalreactor', NULL, '1', '251', '714', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = '18D8F29241668C38351B3CDBA02023B0'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'IV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main west'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'rostik'), 'A1CBF65186EBE2368071E70A28634562', 'multimachine.chemicalreactor', NULL, '3', '260', '709', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = '18D8F29241668C38351B3CDBA02023B0'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'IV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main west'), NULL, 'B2D7145A79D6F841E10A7FEC79ABD2C1', 'multimachine.chemicalreactor', NULL, '3', '171', '777', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = '18D8F29241668C38351B3CDBA02023B0'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'IV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main west'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'kolik'), 'C2B4CF68D3BD7AA93D78291A9967E447', 'multimachine.chemicalreactor', NULL, '4', '0', '0', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = '18D8F29241668C38351B3CDBA02023B0'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'IV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main north'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'kolik'), 'E3D4F668C6C8C4C2F289EE447C913122', 'multimachine.chemicalreactor', NULL, '1', '233', '654', NULL),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = '18D8F29241668C38351B3CDBA02023B0'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'IV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main north'), NULL, '3B61C6B7272B2B43D7354021A25315DD', 'multimachine.vacuumfreezer', NULL, '2', '27', '976', 'upgrade to IV'),
	((SELECT "ID" FROM "db"."oc_computer" WHERE "oc_address" = '18D8F29241668C38351B3CDBA02023B0'), (SELECT "ID" FROM "db"."tier" WHERE "name" = 'IV'), (SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main north'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'rostik'), 'B28111E8146DBFEF1D695AD4E4741971', 'multimachine.vacuumfreezer', NULL, '2', '10', '676', NULL);
  
INSERT INTO "db"."coord" ("x", "y", "z", "DIM", "is_chunk_loaded", "machine_ID") VALUES
	('-7378', '-8016', '24', '128', '0', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = 'D66045A6A3466BA8776A23217FE6A8FA')),
	('-8112', '5693', '4', '1', '0', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = '9CA9A3ED5DFFD30A6738673C088556E7')),
	('2079', '6119', '87', NULL, '0', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = '0F3BED4175EC2E0D26C49339054C7F6B')),
	('530', '-3551', '15', NULL, '0', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = '0B7CC3E7D7A377FB8743C2BDFEC1EC6B')),
	('-4499', '4250', '89', NULL, '1', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = '0C68D49A073668E07ACBB4C7932A5778')),
	('449', '50', '0', '72', '1', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = '54411AC816F36DA974D561EECB9FF5E7')),
	('-2119', '-7654', '19', NULL, '1', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = 'D7AE5B89A2A93BB19BC907314D7108BF')),
	('-3445', '3854', '26', NULL, '0', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = '421972C4D2AE0768682F227845F7B6CA')),
	('-5447', '5893', '49', NULL, '0', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = 'BDDE648F2E2D1D8443E9A87EA89A1012')),
	('2637', '1833', '-17', NULL, '1', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = 'AFF7C31170D5E07680FBA531101CADC6')),
	('-6810', '-9703', '70', NULL, '0', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = 'BD8991493631948CDDC40DCCA5C5686E')),
	('6747', '1941', '38', NULL, '0', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = 'FA4230FA683F36859D126192FC3098DA')),
	('-8879', '836', '56', '38', '1', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = 'B9F673C8069690CBA36CADB07C66301A')),
	('-3630', '-40', '84', NULL, '1', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = '2EC6000A3C7BEA1659D787CFE3A206F4')),
	('-4117', '-3960', '83', NULL, '0', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = '7BA3B38C2614D30E7B638BB7B2CE2DCC')),
	('-3948', '-6086', '23', NULL, '0', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = '8F843FA1E5C2466F69E28A3A778FE64B')),
	('9438', '-1420', '-7', NULL, '0', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = 'ED81F26E2785B426D91DF8166EB90864')),
	('8311', '-8764', '47', '2', '1', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = '6379EE0563C1C7BBAD7904BD0FCF7494')),
	('862', '-4631', '-17', NULL, '1', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = '85EBFB1FE19B4D0E608EAB1FC5584BEC')),
	('-7706', '-6281', '126', NULL, '1', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = 'C68740708B6494AFCAF1ECDE9C4FA8AA')),
	('1417', '-6037', '53', NULL, '1', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = '79F594F938579603E357C3D3DEF79D07')),
	('-5298', '-8570', '5', NULL, '0', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = 'E991DE070F3BE74F8000BED02132F675')),
	('-3381', '-4114', '63', NULL, '1', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = '09F18B74179D2DD3C51590F1B626CD4D')),
	('214', '8092', '65', '9', '1', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = '78BC7D4833801F8F31D0B574C6144914')),
	('9492', '-2456', '-7', NULL, '0', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = '81273683B56C4822E1332BD95523A901')),
	('1536', '183', '9', NULL, '0', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = 'EF95A5CF5DE0A38B7BE2BFE58CDC75B5')),
	('9723', '511', '1', NULL, '0', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = 'E93CC56600B934F98A1F61ABBDD8AABD')),
	('9410', '-324', '23', NULL, '1', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = '0940D4070B32C0FB725C4EA6F7D5C401')),
	('6836', '4181', '64', NULL, '1', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = '1B568F63D6156CF9EA5E251A6A8B297A')),
	('-8207', '-874', '9', NULL, '0', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = '2B1CA797FCA846F163C796EF760C9E90')),
	('1627', '-9428', '78', NULL, '0', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = '36C89F396BAFB062AF7B36C04942EEA8')),
	('6069', '-1836', '0', NULL, '0', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = '7C075ACCF6E1608086DDEF5A65DB0E99')),
	('9888', '-5841', '-17', '55', '1', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = 'C88CD4D8FF09EC47323BB7C27DB4DE94')),
	('9695', '4192', '11', NULL, '0', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = 'B82775282BBEEC348B3CB7EDDCBCC709')),
	('2141', '-4997', '40', NULL, '1', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = '31CDB85FE69AD2673B5A3754A22CFF8F')),
	('-1394', '-9265', '87', NULL, '1', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = 'CEBA86B9EBA9672AEE245FE9E2E4C174')),
	('-6478', '1038', '51', NULL, '1', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = 'AD2EA70F3504EC6CAAB0E3E46315FF7A')),
	('7904', '-2627', '20', '4', '1', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = '9B06C713C5113E9DCAA013B3EB7DE5FE')),
	('4678', '7869', '30', NULL, '1', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = '8FD16A538F0339003FFFD9F1F5C8E915')),
	('-9615', '-7446', '115', NULL, '1', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = 'DEABB2AF779A9525F1AB1C49EDDEA33A')),
	('-7243', '4725', '90', '4', '1', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = 'A908ACC6E21228ACD73C9BDBFDAC9F37')),
	('6625', '438', '-3', NULL, '1', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = 'A63868D0E1269DE815C14081E439DE22')),
	('-3802', '-4556', '118', NULL, '0', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = '3A1804C4C6D18EB69714337A2B524158')),
	('-3814', '9956', '38', NULL, '0', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = 'EC2960B5EAB018786DB72C2DDC524EC0')),
	('-2076', '8516', '46', '2', '0', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = 'A1CBF65186EBE2368071E70A28634562')),
	('-8811', '7195', '124', NULL, '0', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = 'B2D7145A79D6F841E10A7FEC79ABD2C1')),
	('6055', '-1955', '36', NULL, '0', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = 'C2B4CF68D3BD7AA93D78291A9967E447')),
	('-7260', '-2166', '99', '6', '0', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = 'E3D4F668C6C8C4C2F289EE447C913122')),
	('-2885', '-1749', '32', NULL, '0', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = '3B61C6B7272B2B43D7354021A25315DD')),
	('-9404', '-9525', '1', '8', '0', (SELECT "ID" FROM "db"."machine" WHERE "oc_address" = 'B28111E8146DBFEF1D695AD4E4741971'));
    
INSERT INTO "db"."machine_maintenance" ("machine_ID", "maintenance_ID") VALUES
	((SELECT "ID" FROM "db"."machine" WHERE "oc_address" = 'D66045A6A3466BA8776A23217FE6A8FA'), (SELECT "ID" FROM "db"."maintenance" WHERE "message" = 'Something is stuck.')),
    ((SELECT "ID" FROM "db"."machine" WHERE "oc_address" = '0B7CC3E7D7A377FB8743C2BDFEC1EC6B'), (SELECT "ID" FROM "db"."maintenance" WHERE "message" = 'Pipe is loose.')),
    ((SELECT "ID" FROM "db"."machine" WHERE "oc_address" = '0B7CC3E7D7A377FB8743C2BDFEC1EC6B'), (SELECT "ID" FROM "db"."maintenance" WHERE "message" = 'Circuitry burned out.')),
    ((SELECT "ID" FROM "db"."machine" WHERE "oc_address" = 'B9F673C8069690CBA36CADB07C66301A'), (SELECT "ID" FROM "db"."maintenance" WHERE "message" = 'Pipe is loose.')),
    ((SELECT "ID" FROM "db"."machine" WHERE "oc_address" = 'D66045A6A3466BA8776A23217FE6A8FA'), (SELECT "ID" FROM "db"."maintenance" WHERE "message" = 'That doesn''t belong there.')),
    ((SELECT "ID" FROM "db"."machine" WHERE "oc_address" = 'FA4230FA683F36859D126192FC3098DA'), (SELECT "ID" FROM "db"."maintenance" WHERE "message" = 'Platings are dented.'));
    
INSERT INTO "db"."power_source" ("machine_ID", "output_amp", "current_capacity", "max_capacity") VALUES
	((SELECT "ID" FROM "db"."machine" WHERE "oc_address" = '8F843FA1E5C2466F69E28A3A778FE64B'), '1', '37508', '41472'),
	((SELECT "ID" FROM "db"."machine" WHERE "oc_address" = 'ED81F26E2785B426D91DF8166EB90864'), '1', '548', '41472'),
	((SELECT "ID" FROM "db"."machine" WHERE "oc_address" = '6379EE0563C1C7BBAD7904BD0FCF7494'), '1', '32026', '41472'),
	((SELECT "ID" FROM "db"."machine" WHERE "oc_address" = '85EBFB1FE19B4D0E608EAB1FC5584BEC'), '1', '24458', '41472'),
	((SELECT "ID" FROM "db"."machine" WHERE "oc_address" = 'C68740708B6494AFCAF1ECDE9C4FA8AA'), '1', '18201', '41472'),
	((SELECT "ID" FROM "db"."machine" WHERE "oc_address" = '79F594F938579603E357C3D3DEF79D07'), '1', '23215', '41472'),
	((SELECT "ID" FROM "db"."machine" WHERE "oc_address" = 'E991DE070F3BE74F8000BED02132F675'), '1', '6868', '41472'),
	((SELECT "ID" FROM "db"."machine" WHERE "oc_address" = '09F18B74179D2DD3C51590F1B626CD4D'), '1', '23729', '41472');
    
INSERT INTO "db"."power_network_power_source" ("power_network_ID", "power_source_ID", "is_stable") VALUES
	((SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main north'), (SELECT pw."ID" FROM "db"."power_source" pw LEFT JOIN "db"."machine" m ON pw."machine_ID" = m."ID"  WHERE "oc_address" = '8F843FA1E5C2466F69E28A3A778FE64B'), NULL),
	((SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main north'), (SELECT pw."ID" FROM "db"."power_source" pw LEFT JOIN "db"."machine" m ON pw."machine_ID" = m."ID"  WHERE "oc_address" = 'ED81F26E2785B426D91DF8166EB90864'), '0'),
	((SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main north'), (SELECT pw."ID" FROM "db"."power_source" pw LEFT JOIN "db"."machine" m ON pw."machine_ID" = m."ID"  WHERE "oc_address" = '6379EE0563C1C7BBAD7904BD0FCF7494'), NULL),
	((SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main north'), (SELECT pw."ID" FROM "db"."power_source" pw LEFT JOIN "db"."machine" m ON pw."machine_ID" = m."ID"  WHERE "oc_address" = '85EBFB1FE19B4D0E608EAB1FC5584BEC'), NULL),
	((SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main north'), (SELECT pw."ID" FROM "db"."power_source" pw LEFT JOIN "db"."machine" m ON pw."machine_ID" = m."ID"  WHERE "oc_address" = 'C68740708B6494AFCAF1ECDE9C4FA8AA'), '0'),
	((SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main north'), (SELECT pw."ID" FROM "db"."power_source" pw LEFT JOIN "db"."machine" m ON pw."machine_ID" = m."ID"  WHERE "oc_address" = '79F594F938579603E357C3D3DEF79D07'), NULL),
	((SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main north'), (SELECT pw."ID" FROM "db"."power_source" pw LEFT JOIN "db"."machine" m ON pw."machine_ID" = m."ID"  WHERE "oc_address" = 'E991DE070F3BE74F8000BED02132F675'), NULL),
	((SELECT "ID" FROM "db"."power_network" WHERE "name" = 'main north'), (SELECT pw."ID" FROM "db"."power_source" pw LEFT JOIN "db"."machine" m ON pw."machine_ID" = m."ID"  WHERE "oc_address" = '09F18B74179D2DD3C51590F1B626CD4D'), NULL);
    
INSERT INTO "db"."machine_control" ("machine_ID", "control_ID", "user_ID") VALUES
	((SELECT "ID" FROM "db"."machine" WHERE "oc_address" = 'D66045A6A3466BA8776A23217FE6A8FA'), (SELECT "ID" FROM "db"."control" WHERE "name" = 'Manual Machine Operation'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'pepik')),
	((SELECT "ID" FROM "db"."machine" WHERE "oc_address" = 'D66045A6A3466BA8776A23217FE6A8FA'), (SELECT "ID" FROM "db"."control" WHERE "name" = 'Remote Control'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'pepik')),
	((SELECT "ID" FROM "db"."machine" WHERE "oc_address" = '0B7CC3E7D7A377FB8743C2BDFEC1EC6B'), (SELECT "ID" FROM "db"."control" WHERE "name" = 'Automatic Recipe Crafting Mode'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'bobik')),
	((SELECT "ID" FROM "db"."machine" WHERE "oc_address" = '0B7CC3E7D7A377FB8743C2BDFEC1EC6B'), (SELECT "ID" FROM "db"."control" WHERE "name" = 'Remote Control'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'bobik')),
	((SELECT "ID" FROM "db"."machine" WHERE "oc_address" = 'AFF7C31170D5E07680FBA531101CADC6'), (SELECT "ID" FROM "db"."control" WHERE "name" = 'Automatic Production Mode'), (SELECT "ID" FROM "db"."user" WHERE "nickname" = 'bobik'));
    