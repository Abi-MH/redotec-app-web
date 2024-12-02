import os
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# Asegúrate de que tu archivo de credenciales de Google esté configurado correctamente
def get_drive_service():
    creds = Credentials.from_service_account_file(
        'path_to_your_google_service_account_credentials.json',
        scopes=["https://www.googleapis.com/auth/drive.file"]
    )
    service = build('drive', 'v3', credentials=creds)
    return service

def upload_to_drive(file_path, file_name):
    # Obtener servicio de Google Drive
    service = get_drive_service()

    # Crear un archivo en Google Drive
    file_metadata = {
        'name': file_name,
        'mimeType': 'application/pdf' if file_name.endswith('.pdf') else 'application/octet-stream'
    }
    media = MediaFileUpload(file_path, mimetype='application/pdf')

    # Subir el archivo
    file = service.files().create(
        media_body=media,
        body=file_metadata
    ).execute()

    # Retorna el ID del archivo subido en Google Drive
    return file['id']
