#built-in

#third-parties
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import psycopg2

#custom
from lake_google_drive_access.google_drive_connect import get_file
from database_access.postgres_connect import get_database_credentials

try:
    truncate_table = """TRUNCATE TABLE "STAGE_PASSEI_DIRETO".stg_dim_courses"""
    connection = get_database_credentials()
    cursor = connection.cursor()
    cursor.execute(truncate_table)

    records_list = get_file('courses.json')

    for record in records_list:
        postgres_insert_query = """ INSERT INTO "STAGE_PASSEI_DIRETO".stg_dim_courses
                                    (id, "name")
                                    VALUES(%s,%s);"""
        record_to_insert = (record['Id'] if 'Id' in record else None, 
                            record['Name'] if 'Name' in record else None)
        cursor.execute(postgres_insert_query, record_to_insert)

    connection.commit()
    count = cursor.rowcount
    print (count, "Record inserted successfully")
except (Exception, psycopg2.Error) as error:
    print ("Error while processing", error)
finally:
    cursor.close()
    connection.close()
    print("PostgreSQL connection is closed")



