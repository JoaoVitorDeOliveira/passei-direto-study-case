
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json

from loguru import logger
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from sidebar import sidebar_data
from page import page_data


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

file_list = drive.ListFile({'q': "'143WlS7ryr2w6wmNIeR_AGGdQ9_bPXUnm' in parents and trashed=false"}).GetList()
records_list = []

for file1 in file_list: 
    file1.GetContentFile(file1['title'])

print(records_list)
st.set_option('deprecation.showfileUploaderEncoding', False)
st.set_option('deprecation.showPyplotGlobalUse', False)
logger.info("Start process")

df_contry = pd.read_csv('country.csv')
df_user = pd.read_csv('users.csv')
df_full = pd.read_csv('full.csv')

df_contry = df_contry[df_contry['count'] > 100]

logger.success("Loaded file")

st.sidebar.markdown('''
Esse é uma plataforma para análise prévia 
dos dados de um dataset.
''')

logger.info("Loading table")

logger.info("Loading sidebar")
#sidebar_data.initial_data_processing(df_full)

df_full.groupby('state').size()

aux = list(df_full.groupby('state').size())
size = [float(i) for i in aux]
labels = tuple(df_full['state'].dropna().unique())

st.title('Usuários por região com base nos Eventos da PD')
fig1, ax1 = plt.subplots()
ax1.pie(size, labels=labels,  autopct='%1.1f%%', 
            shadow=True, startangle=90)
ax1.axis('equal')
st.pyplot()

st.title('Países estrangeiros com mais de 100 acessos')
plt.bar(df_contry['country'], df_contry['count'])
st.pyplot()

st.title('Quantidade de usuários por tipo')
plt.bar(df_user['custom_4'], df_user['count'])
st.pyplot()







