import json

import psycopg2
from loguru import logger
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
            body = file1.GetContentString()
            records_list = json.loads(body)

    return records_list

def get_unstructured_file():
    drive = _google_connect()

    file_list = drive.ListFile({'q': "'1mmJbjh4LznzE9EcMHF4E4RUkxjGz0t2Y' in parents and trashed=false"}).GetList()
    records_list = []

    for file1 in file_list: 
        if file1['title'] == 'part-00000.json':
            logger.debug('Processing File {}'.format(file1['title']))
            body = file1.GetContentString().split('\n')
            records_list += body

    logger.debug('Size records: {}'.format(len(records_list)))
    print(records_list[0])
    return records_list


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