import os
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from tasks.google_drive_utils import download_file_from_drive

# Asegúrate de que tu archivo de credenciales de Google esté configurado correctamente
def get_drive_service():
    # Leer la ruta del archivo de credenciales desde la variable de entorno
    credentials_path = os.getenv('GOOGLE_DRIVE_CREDENTIALS_PATH')
    
    # Verifica que el archivo de credenciales esté presente
    if not credentials_path:
        raise ValueError("El archivo de credenciales de Google no está configurado correctamente.")
    
    # Autenticación
    creds = Credentials.from_service_account_file(credentials_path, scopes=['https://www.googleapis.com/auth/drive'])
    
    # Crear el servicio de Google Drive
    service = build('drive', 'v3', credentials=creds)
    return service

def set_file_public(file_id):
    try:
        service = get_drive_service()
        # Actualizar los permisos para hacer el archivo público
        permissions = {
            'role': 'reader',  # Para que sea público, debe ser "reader"
            'type': 'anyone'   # 'anyone' significa cualquier persona puede ver el archivo
        }
        # Crear el permiso
        service.permissions().create(
            fileId=file_id,
            body=permissions
        ).execute()
        print(f"Archivo con ID {file_id} ahora es público.")
    except HttpError as error:
        print(f"An error occurred while setting file as public: {error}")

def upload_to_drive(file_path, file_name):
    try:
        service = get_drive_service()
        
        # Abre el archivo y crea la metadata
        file_metadata = {'name': file_name}
        media = MediaFileUpload(file_path, resumable=True)

        # Subir el archivo a Drive
        request = service.files().create(media_body=media, body=file_metadata)
        file = request.execute()

        # Hacer el archivo público
        set_file_public(file['id'])
        return file
    except HttpError as error:
        print(f"An error occurred: {error}")
