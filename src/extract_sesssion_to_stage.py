#built-in

#third-parties
from loguru import logger

#custom
from lake_google_drive_access.google_drive_connect import get_file
from database_access.postgres_connect import get_database_credentials

@logger.catch
def main():
    try:
        truncate_table = """TRUNCATE TABLE "STAGE_PASSEI_DIRETO".stg_dim_sessions"""

        connection = get_database_credentials()
        logger.debug("Get the database credentials")

        cursor = connection.cursor()
        cursor.execute(truncate_table)
        logger.debug("Truncate Table STG_DIM_SESSIONS")

        records_list = get_file('sessions.json')
        logger.debug('Retrieved {} records from file "sessions.json"'.format(len(records_list)))

        #Heroku databse has 10000 limits line, so I will retrieve only 500 lines from the files
        for record in records_list[0:500]:
            postgres_insert_query = """ INSERT INTO "STAGE_PASSEI_DIRETO".stg_dim_sessions
                                        (student_id, start_time, student_client)
                                        VALUES(%s,%s,%s);"""
            record_to_insert = (record['StudentId'] if 'StudentId' in record else None, 
                                record['SessionStartTime'] if 'SessionStartTime' in record else None,
                                record['StudentClient'] if 'StudentClient' in record else None)
            cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        logger.debug("Records inserted successfully")
    except (Exception) as error :
        logger.error("Error while connecting to PostgreSQL: {}".format(error))
    finally:
        #closing database connection.
        cursor.close()
        connection.close()
        logger.warning("PostgreSQL connection is closed")

if __name__ == '__main__':
    main()


  