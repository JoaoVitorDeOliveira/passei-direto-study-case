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

file1 = drive.CreateFile({'parents': [{'kind': 'drive#fileLink', 'id': '143WlS7ryr2w6wmNIeR_AGGdQ9_bPXUnm'}]})
file1.SetContentFile('./result/part-00000-92f59061-e8f5-4030-a248-127bd537065f-c000.csv')
file1.Upload()
  
