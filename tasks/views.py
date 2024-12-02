from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from django.http import HttpResponse
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials
import os
from django.conf import settings
from .google_drive_utils import upload_to_drive  # Asegúrate de que esta función esté importada correctamente.


# Create your views here.
#def hello(request):
 #   return render(request, 'signup.html',
  #                {'form':UserCreationForm})
 #usaremos los forms que trae django
 #  para utilizar esta tecnologia que lo integra
def home (request):
    return render(request,'home.html')

def signup (request):
    if request.method== 'GET':
        return render(request, 'signup.html',{
            'form':UserCreationForm
        })
    else:
        if request.POST['password1']==request.POST['password2']:            
            try:
                #registro de usuario
                user = User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
                #return HttpResponse('Usuario creado correctamente')
            except IntegrityError:    
               return render(request, 'signup.html',{
            'form':UserCreationForm,
            "error":'El usuario ya existe'
        })     
        return render(request, 'signup.html',{
            'form':UserCreationForm,
            "error":'Las contraseñas no coinciden'
        })

@login_required
def tasks(request):
    # Cambié 'task' a 'tasks' para que coincida con el contexto
   # tasks = Task.objects.all()   # Obtener todas las tareas
    #return render(request, 'tasks.html', {'tasks': tasks})  # Pasar la variable correcta al contexto
    # Filtra las tareas que no están completadas
    tasks = Task.objects.filter(datecompleted__isnull=True)
    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def tasks_completed(request):
    # Cambié 'task' a 'tasks' para que coincida con el contexto
   # tasks = Task.objects.all()   # Obtener todas las tareas
    #return render(request, 'tasks.html', {'tasks': tasks})  # Pasar la variable correcta al contexto
    # Filtra las tareas que no están completadas
    tasks = Task.objects.filter(datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks_completed.html', {'tasks': tasks})

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.user = request.user

            # Subir archivo PDF a Google Drive
            if new_task.payment_pdf:
                file_path = new_task.payment_pdf.path
                file_name = new_task.payment_pdf.name
                file_id_pdf = upload_to_drive(file_path, file_name)
                # Puedes almacenar el file_id_pdf si lo necesitas en el modelo

            # Subir archivo de imagen a Google Drive
            if new_task.payment_image:
                file_path = new_task.payment_image.path
                file_name = new_task.payment_image.name
                file_id_image = upload_to_drive(file_path, file_name)
                # Puedes almacenar el file_id_image si lo necesitas en el modelo

            # Subir archivo XML a Google Drive
            if new_task.payment_xml:
                file_path = new_task.payment_xml.path
                file_name = new_task.payment_xml.name
                file_id_xml = upload_to_drive(file_path, file_name)
                # Puedes almacenar el file_id_xml si lo necesitas en el modelo

            new_task.save()
            return redirect('tasks')
    return render(request, 'create_task.html', {'form': TaskForm()})

          
@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)  # Obtén la tarea existente

    if request.method == 'GET':
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {
            'task': task, 
            'form': form,
            'is_completed': task.datecompleted is not None,  # Determina si está completada
        })
    else:
        try:
            # Maneja datos POST y archivos
            form = TaskForm(request.POST, request.FILES, instance=task)
            
            if form.is_valid():
                form.save()
                return redirect('tasks')
            else:
                return render(request, 'task_detail.html', {
                    'task': task,
                    'form': form,
                    'is_completed': task.datecompleted is not None,
                    'error': "El formulario tiene errores. Revisa los campos."
                })
        except ValueError:
            return render(request, 'task_detail.html', {
                'task': task,
                'form': form,
                'is_completed': task.datecompleted is not None,
                'error': "No se pudo actualizar la tarea. Intenta nuevamente."
            })

# Vista para marcar la tarea como completada
@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('task_detail', task_id=task_id)
    
# Vista para desmarcar la tarea como completada (esto es lo que necesitas)
@login_required
def uncomplete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        task.datecompleted = None
        task.save()
        return redirect('task_detail', task_id=task_id)

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)    
    
    if request.method == 'POST':
        # Marcar la tarea como eliminada
        task.delete()
        
        # Redirige a la vista de tareas (se refrescará y no mostrará la tarea eliminada)
        return redirect('tasks')

@login_required
def signout (request):
    logout(request)
    return redirect ('home')

def signin(request):
    if request.method == 'GET':
        return render(request,'signin.html',{
        'form':AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request,'signin.html',{
            'form':AuthenticationForm,
            'error':'El usuario o contraseña son incorrectas'
        })
        else:
            login(request, user)#Guardamos la sesion si todo esta bien
            return redirect('tasks')        
            
@login_required
def task_list(request):
    tasks_pending = Task.objects.filter(datecompleted__isnull=True)
    tasks_completed = Task.objects.filter(datecompleted__isnull=False)
    return render(request, 'task_list.html', {
        'tasks_pending': tasks_pending,
        'tasks_completed': tasks_completed,
    })

@login_required
def upload_to_drive(file_path, file_name, folder_id=None):
    """ Sube un archivo a Google Drive.
    :param file_path: Ruta local del archivo.
    :param file_name: Nombre del archivo en Google Drive.
    :param folder_id: ID de la carpeta en Google Drive (opcional).
    :return: ID del archivo subido.
    """
    # Ruta al archivo temporal de credenciales
    credentials_path = os.path.join(settings.BASE_DIR, 'google-drive-service-account.json')

    # Carga las credenciales
    credentials = Credentials.from_service_account_file(credentials_path)
    drive_service = build('drive', 'v3', credentials=credentials)

    # Metadatos del archivo
    file_metadata = {'name': file_name}
    if folder_id:
        file_metadata['parents'] = [folder_id]

    # Preparar el archivo para subir
    media = MediaFileUpload(file_path, resumable=True)

    # Subir el archivo
    file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    return file.get('id')

@login_required
def set_file_public(file_id):
    """
    Hace que un archivo sea público.
    :param file_id: ID del archivo en Google Drive.
    """
    # Ruta al archivo temporal de credenciales
    credentials_path = os.path.join(settings.BASE_DIR, 'google-drive-service-account.json')

    # Carga las credenciales
    credentials = Credentials.from_service_account_file(credentials_path)
    drive_service = build('drive', 'v3', credentials=credentials)

    # Crear el permiso
    permission = {
        'type': 'anyone',
        'role': 'reader'
    }

    # Aplicar el permiso
    drive_service.permissions().create(
        fileId=file_id,
        body=permission
    ).execute()