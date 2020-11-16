#built-in
import sys

#third-parties
from loguru import logger

#custom
from database_access.postgres_connect import get_database_credentials

@logger.catch
def main():
    try:
        logger.debug('Loading file: {}'.format(sys.argv[1]))
        with open('../sql/{}'.format(sys.argv[1]), 'r') as query:
            connection = get_database_credentials()
            logger.debug("Get the database credentials")
            cursor = connection.cursor()
            cursor.execute(query.read())
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


  