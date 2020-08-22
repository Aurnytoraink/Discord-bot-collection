import pickle
import os.path
import io
import random
from pathlib import Path
# Install this before
# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaIoBaseDownload
from google.auth.transport.requests import Request
from urllib.parse import urlparse

# TODO Télécharger les 5 premières musiques du dossier pour éviter des trop gros temps de chargement

PATH = Path("/home/aurnytoraink/Projets/Code/Bot/Diskcord/") # <= Put your path
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def login():
    creds = None

    if os.path.exists(PATH / 'token.pickle'):
        with open(PATH / 'token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                (PATH / 'Gcredentials.json'), SCOPES) # <= To get this file, refer to the GDrive API documentation
            creds = flow.run_local_server(port=0)
        with open(PATH / 'token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)
    print("Google connected!")
    return service

def getMedias(service, url, shuffle=False):
    queudlist = []
    if url.startswith("https://drive.google.com/drive/folders/"):
        folderId = urlparse(url).path.split("/")[3]
        results = service.files().list(
            q="'{}' in parents".format(folderId), fields="files(id,mimeType,name)", orderBy="name", pageSize=1000
        ).execute()
        results = results.get('files', [])
        if not results:
            print('No files found.')
            return None
        else:
            for element in results:
                if element["mimeType"].startswith("audio"):
                    queudlist.append([element["id"],element["name"]])
            if shuffle:
                random.shuffle(queudlist)
        return queudlist

    elif url.startswith("https://drive.google.com/file/d/"):
        fileId = urlparse(url).path.split("/")[3]
        queudlist.append(fileId)
        return queudlist

def downloadMedia(service, fileId, vcId):
    if os.path.exists(PATH / ('musics/'+vcId+'/'+fileId)):
        print("File already downloaded")
        return
    else:
        if os.path.exists(PATH / ('musics/'+vcId)) == False:
            os.makedirs(PATH / ('musics/'+vcId))
        request = service.files().get_media(fileId=fileId)
        output = io.FileIO(PATH / ('musics/'+vcId+'/'+fileId),'wb')
        downloader = MediaIoBaseDownload(output, request)
        done = False
        while done is False:
           done = downloader.next_chunk()[1]