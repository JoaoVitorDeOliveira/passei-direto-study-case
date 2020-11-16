import json
import glob

import psycopg2
#from loguru import logger
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def get_file(file):
    """Get all files from the transactional folder and filter to the one passed as argument

    Args:
        file ([string]): [file to retrieve]

    Returns:
        [list]: [all records from the file as a list]
    """      
    drive = _google_connect()

    file_list = drive.ListFile({'q': "'1IcIskimW45heqv-tS8w4siyZhtO9Okkm' in parents and trashed=false"}).GetList()
    records_list = []

    for file1 in file_list: 
        if file1['title'] == file:
            #logger.debug('Get {} records'.format(file1['title']))
            body = file1.GetContentString()
            records_list = json.loads(body)
    #Heroku databse has 10000 limits line, so I will retrieve only 500 lines from the files
    return records_list[:500]

def get_unstructured_file():
    """Get all Events Files from Raw
    """    
    drive = _google_connect()

    file_list = drive.ListFile({'q': "'1qmyyIJnRK_c6tZP_s5Rsk1zz1p1JI73A' in parents and trashed=false"}).GetList()

    for file1 in file_list: 
        #logger.debug('Processing File {}'.format(file1['title']))
        file1.GetContentFile(file1['title'])
    
def send_files(path):
    """Send CSV Generated files to Drive

    Args:
        path ([string]): [path of the csv files]
    """    
    drive = _google_connect()

    csv_files = glob.glob(path)
    for csv in csv_files:
        file1 = drive.CreateFile({'parents': [{'kind': 'drive#fileLink', 'id': '143WlS7ryr2w6wmNIeR_AGGdQ9_bPXUnm'}]})
        #logger.debug("Sending {} file...".format(csv))
        file1.SetContentFile(csv)
        file1.Upload()
        #logger.success("Done!!")

def _google_connect():
    """Get the credentials from Google Drive, with 'mycreds.txt' file we can access
    without the need of logging through web

    Returns:
        [driver]: [Driver to access Google Drive files]
    """    
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

    return drive