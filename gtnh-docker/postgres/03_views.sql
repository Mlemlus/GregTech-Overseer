------- VIEWS -----------
CREATE OR REPLACE VIEW "gtoverseer"."machine_report" AS
SELECT
m."ID" AS "ID",
COALESCE(m."custom_name", m."name") AS "name",
t."name" AS tier,
m."amp" AS amp,
pn."name" AS power_network_name,
CONCAT('X:', c."x", ' Y:', c."y", ' Z:', c."z") AS coord,
c."is_chunk_loaded" AS chunk_loaded,
COALESCE(mm."is_fixed",TRUE) AS is_operational,
case
	WHEN  w."work_progress_max" = 0 then 0
	else ((w."work_progress"::FLOAT / w."work_progress_max") * 100)
end AS "work_progress",
m."created_at" AS created_at,
m."oc_address" AS oc_address,
m."note" AS note
FROM "gtoverseer"."machine" m
LEFT JOIN "gtoverseer"."coord" c ON m."ID" = c."machine_ID"
LEFT JOIN "gtoverseer"."work" w ON m."ID" = w."machine_ID"
LEFT JOIN "gtoverseer"."machine_maintenance" mm ON m."ID" = mm."machine_ID"
LEFT JOIN "gtoverseer"."power_network" pn ON m."power_network_ID" = pn."ID"
LEFT JOIN "gtoverseer"."tier" t ON m."tier_ID" = t."ID"
WHERE m."is_connected" = TRUE;