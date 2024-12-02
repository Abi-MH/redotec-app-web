from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials
import os

# Carga las credenciales desde settings
from django.conf import settings

def upload_to_drive(file_path, file_name, folder_id=None):
    """
    Sube un archivo a Google Drive.
    :param file_path: Ruta local del archivo.
    :param file_name: Nombre del archivo en Google Drive.
    :param folder_id: ID de la carpeta en Google Drive (opcional).
    :return: ID del archivo subido.
    """
    credentials = Credentials.from_service_account_file(settings.GOOGLE_DRIVE_CREDENTIALS)
    drive_service = build('drive', 'v3', credentials=credentials)

    file_metadata = {'name': file_name}
    if folder_id:
        file_metadata['parents'] = [folder_id]

    media = MediaFileUpload(file_path, resumable=True)

    file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    return file.get('id')


def set_file_public(file_id):
    """
    Hace que un archivo sea público.
    :param file_id: ID del archivo en Google Drive.
    """
    credentials = Credentials.from_service_account_file(settings.GOOGLE_DRIVE_CREDENTIALS)
    drive_service = build('drive', 'v3', credentials=credentials)

    permission = {
        'type': 'anyone',
        'role': 'reader'
    }
    drive_service.permissions().create(
        fileId=file_id,
        body=permission
    ).execute()
