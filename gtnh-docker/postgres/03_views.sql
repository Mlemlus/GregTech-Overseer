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