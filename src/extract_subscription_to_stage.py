#built-in

#third-parties
from loguru import logger

#custom
from lake_google_drive_access.google_drive_connect import get_file
from database_access.postgres_connect import get_database_credentials

@logger.catch
def main():
    try:
        truncate_table = """TRUNCATE TABLE "STAGE_PASSEI_DIRETO".stg_dim_subscriptions"""

        connection = get_database_credentials()
        logger.debug("Get the database credentials")

        cursor = connection.cursor()
        cursor.execute(truncate_table)
        logger.debug("Truncate Table stg_dim_subscriptions")

        records_list = get_file('subscriptions.json')
        logger.debug('Retrieved {} records from file "subscriptions.json"'.format(len(records_list)))
        logger.debug('Inserting records...')
        for record in records_list:
            postgres_insert_query = """ INSERT INTO "STAGE_PASSEI_DIRETO".stg_dim_subscriptions
                                        (student_id, payment_date, plan_type)
                                        VALUES(%s,%s,%s);"""
            record_to_insert = (record['StudentId'] if 'StudentId' in record else None, 
                                record['PaymentDate'] if 'PaymentDate' in record else None,
                                record['PlanType'] if 'PlanType' in record else None)
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