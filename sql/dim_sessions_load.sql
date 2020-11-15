---- Source ----
WITH CTE AS (
	SELECT COALESCE(student_id, 'N/A') student_id,
	CAST(COALESCE(start_time, '1900-01-01 00:00:0000') AS TIMESTAMP) start_time,
	COALESCE(student_client, 'N/A') student_client 
	FROM "STAGE_PASSEI_DIRETO".stg_dim_sessions
	ORDER BY student_id
    )
-----------------
---- Target ----
    INSERT INTO "DM_PASSEI_DIRETO".dim_sessions
    SELECT * FROM CTE
----------------