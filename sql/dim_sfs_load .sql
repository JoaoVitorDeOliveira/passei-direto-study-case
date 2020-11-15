---- Source ----
WITH CTE AS (
	SELECT COALESCE(student_id, 'N/A') student_id,
	CAST(COALESCE(subject_id, '-1') AS INT) subject_id,
	CAST(COALESCE(follow_date, '1900-01-01 00:00:0000') AS TIMESTAMP) follow_date	 
	FROM "STAGE_PASSEI_DIRETO".stg_dim_student_follow_subject sdsfs 
	ORDER BY student_id
    )
-----------------
---- Target ----
    INSERT INTO "DM_PASSEI_DIRETO".dim_student_follow_subject
    SELECT * FROM CTE
----------------