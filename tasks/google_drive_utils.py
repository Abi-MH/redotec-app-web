import os
<<<<<<< HEAD
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

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
=======
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from googleapiclient.errors import HttpError
# Asegúrate de que tu archivo de credenciales de Google esté configurado correctamente
import os
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

def get_drive_service():
    # Leer la ruta del archivo de credenciales desde la variable de entorno
    credentials_path = os.getenv('GOOGLE_DRIVE_CREDENTIALS_PATH')
    if not credentials_path:
        raise ValueError("La variable de entorno GOOGLE_DRIVE_CREDENTIALS_PATH no está configurada correctamente.")
    
    # Crear credenciales desde el archivo
    creds = Credentials.from_service_account_file(
        credentials_path,
        scopes=["https://www.googleapis.com/auth/drive.file"]
    )
    # Construir el servicio de Google Drive
>>>>>>> cdca48917fe2ba1200cfa74bf017b4d18711eeb8
    service = build('drive', 'v3', credentials=creds)
    return service

def set_file_public(file_id):
    try:
        service = get_drive_service()
<<<<<<< HEAD
=======

>>>>>>> cdca48917fe2ba1200cfa74bf017b4d18711eeb8
        # Actualizar los permisos para hacer el archivo público
        permissions = {
            'role': 'reader',  # Para que sea público, debe ser "reader"
            'type': 'anyone'   # 'anyone' significa cualquier persona puede ver el archivo
        }
<<<<<<< HEAD
=======

>>>>>>> cdca48917fe2ba1200cfa74bf017b4d18711eeb8
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
<<<<<<< HEAD
        
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
=======

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

        file_id = file['id']  # Devuelve el ID del archivo subido
        print(f"Archivo subido con éxito. ID del archivo: {file_id}")  # Imprimir el ID del archivo

        # Asegurarse de que el archivo sea público
        set_file_public(file_id)

        return file_id  # Retorna el ID del archivo subido
    except HttpError as error:
        print(f"An error occurred while uploading the file to Google Drive: {error}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
>>>>>>> cdca48917fe2ba1200cfa74bf017b4d18711eeb8
