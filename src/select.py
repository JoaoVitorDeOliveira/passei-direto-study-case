import json

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import psycopg2



try: 
    connection = psycopg2.connect(user = "hkmwrxkewkhzrh",
                                    password = "a8f37ea49b38f2d3d07d853b15ed59e0a7b5edaea657c3450c970dd8b9038a57",
                                    host = "ec2-54-91-178-234.compute-1.amazonaws.com",
                                    port = "5432",
                                    database = "de6eje61ar0ot3")

    cursor = connection.cursor()

    postgres_insert_query = """ SELECT * FROM "STAGE_PASSEI_DIRETO".stg_dim_courses
                                    """
        #record_to_insert = (student['Id'] if 'Id' in student else None, 
        #                    student['Name'] if 'Name' in student else None)
    cursor.execute(postgres_insert_query)
    courses = cursor.fetchall() 
    print (type(courses))
except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


  
