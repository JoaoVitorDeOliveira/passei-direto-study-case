---- Source ----
WITH CTE AS (
	SELECT CAST(COALESCE(id, '-1') AS INT) id,
	COALESCE("name", 'N/A') "name"
	FROM "STAGE_PASSEI_DIRETO".stg_dim_courses
	ORDER BY id
    ),
-----------------
---- Slow Change Dimession ----
    UPD AS (
        UPDATE "DM_PASSEI_DIRETO".dim_courses T
        SET    change_date = current_date
        FROM   CTE
        WHERE  (T.id = CTE.id AND T.change_date IS NULL) 
                AND T."name" <> CTE."name"
        RETURNING T.id
    )
--------------------------------
---- Target ----
    INSERT INTO "DM_PASSEI_DIRETO".dim_courses(id, "name", change_date )
    SELECT id, "name", NULL FROM CTE
    WHERE CTE.id IN (SELECT id FROM UPD) OR
        CTE.id NOT IN (SELECT id FROM "DM_PASSEI_DIRETO".dim_courses)
----------------