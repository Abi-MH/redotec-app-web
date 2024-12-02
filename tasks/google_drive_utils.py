import os
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from googleapiclient.errors import HttpError

# Asegúrate de que tu archivo de credenciales de Google esté configurado correctamente
def get_drive_service():
    creds = Credentials.from_service_account_file(
        'path_to_your_google_service_account_credentials.json',
        scopes=["https://www.googleapis.com/auth/drive.file"]
    )
    service = build('drive', 'v3', credentials=creds)
    return service

def upload_to_drive(file_path, file_name):
    try:
        service = get_drive_service()

        # Crear metadatos del archivo
        file_metadata = {
            'name': file_name,
            'mimeType': 'application/octet-stream'
        }

        # Determina el tipo de archivo (para imágenes u otros tipos)
        if file_name.endswith('.jpg') or file_name.endswith('.jpeg') or file_name.endswith('.png'):
            mime_type = 'image/jpeg' if file_name.endswith('.jpg') else 'image/png'
        else:
            mime_type = 'application/octet-stream'

        # Preparar archivo para subir
        media = MediaFileUpload(file_path, mimetype=mime_type)

        # Subir el archivo a Google Drive
        file = service.files().create(
            media_body=media,
            body=file_metadata
        ).execute()

        return file['id']  # Devuelve el ID del archivo subido
    except HttpError as error:
        print(f"An error occurred while uploading the file to Google Drive: {error}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None