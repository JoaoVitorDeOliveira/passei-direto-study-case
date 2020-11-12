---- Source ----
WITH CTE AS (
	SELECT COALESCE(id, 'N/A') id,
	CAST(COALESCE(registered_data, '1900-01-01') AS DATE) registered_data, 
	COALESCE(state, 'N/A') state,
	COALESCE(city, 'N/A') city, 
	CAST(COALESCE(university_id, '-1') AS INT) university_id, 
	CAST(COALESCE(course_id, '-1') AS INT) course_id, 
	COALESCE(signup_source, 'N/A') signup_source 
	FROM "STAGE_PASSEI_DIRETO".stg_fat_students 
	ORDER BY ID
    ),
-----------------
---- Slow Change Dimession ----
    UPD AS (
        UPDATE "DM_PASSEI_DIRETO".fat_students T
        SET    change_date = current_date
        FROM   CTE
        WHERE  (T.id = CTE.id AND T.change_date IS NULL) 
                AND (T.state <> CTE.state OR T.city <> CTE.city OR T.university_id <> CTE.university_id OR T.course_id <> CTE.course_id)
        RETURNING T.id
    )
--------------------------------
---- Target ----
    INSERT INTO "DM_PASSEI_DIRETO".fat_students(id, registered_data, state, city, university_id, course_id, signup_source, change_date)
    SELECT id, registered_data, state, city, university_id, course_id, signup_source, NULL FROM CTE
    WHERE CTE.id IN (SELECT id FROM UPD) OR
        CTE.id NOT IN (SELECT id FROM "DM_PASSEI_DIRETO".fat_students)
----------------