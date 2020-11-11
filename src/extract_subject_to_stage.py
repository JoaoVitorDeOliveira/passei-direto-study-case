import json

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import psycopg2


gauth = GoogleAuth()
# Try to load saved client credentials
gauth.LoadCredentialsFile("mycreds.txt")
if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile("mycreds.txt")
drive = GoogleDrive(gauth)


file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
students_list = []

for file1 in file_list:
    if file1['title'] == 'subjects.json':
        body = file1.GetContentString()
        students_list = json.loads(body)
        print(len(students_list))

try: 
    connection = psycopg2.connect(user = "hkmwrxkewkhzrh",
                                    password = "a8f37ea49b38f2d3d07d853b15ed59e0a7b5edaea657c3450c970dd8b9038a57",
                                    host = "ec2-54-91-178-234.compute-1.amazonaws.com",
                                    port = "5432",
                                    database = "de6eje61ar0ot3")

    cursor = connection.cursor()
    for student in students_list[0:500]:
        postgres_insert_query = """ INSERT INTO "STAGE_PASSEI_DIRETO".stg_dim_subjects
                                    (id, "name")
                                    VALUES(%s,%s);"""
        record_to_insert = (student['Id'] if 'Id' in student else None, 
                            student['Name'] if 'Name' in student else None)
        cursor.execute(postgres_insert_query, record_to_insert)
    connection.commit()
    count = cursor.rowcount
    print (count, "Record inserted successfully")
except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


  