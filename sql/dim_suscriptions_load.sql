---- Source ----
WITH CTE AS (
	SELECT COALESCE(student_id, 'N/A') student_id,
	CAST(COALESCE(payment_date, '1900-01-01 00:00:0000') AS TIMESTAMP) payment_date,
	COALESCE(plan_type, 'N/A') plan_type 
	FROM "STAGE_PASSEI_DIRETO".stg_dim_subscriptions
	ORDER BY student_id
    )
-----------------
---- Target ----
    INSERT INTO "DM_PASSEI_DIRETO".dim_subscriptions
    SELECT * FROM CTE