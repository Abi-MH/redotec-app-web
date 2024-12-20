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

# Create your views here.
def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:            
            try:
                # Registro de usuario
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:    
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'El usuario ya existe'
                })     
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Las contraseñas no coinciden'
        })

@login_required
def tasks(request):
    tasks = Task.objects.filter(datecompleted__isnull=True)
    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks_completed.html', {'tasks': tasks})

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {'form': TaskForm()})
    else:
        try:
            form = TaskForm(request.POST, request.FILES)  # Asegúrate de que los archivos se manejen aquí
            if form.is_valid():
                new_task = form.save(commit=False)
                new_task.user = request.user
                new_task.save()
                return redirect('tasks')
            else:
                return render(request, 'create_task.html', {
                    'form': form,
                    'error': 'Por favor, ingresa campos válidos.'
                })
        except ValueError:
            return render(request, 'create_task.html', {
                'form': form,
                'error': 'No se pudo guardar la tarea. Intenta nuevamente.'
            })

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if request.method == 'GET':
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {
            'task': task, 
            'form': form,
            'is_completed': task.datecompleted is not None,
        })
    else:
        try:
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

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('task_detail', task_id=task_id)

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
        task.delete()
        return redirect('tasks')

@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {'form': AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {'form': AuthenticationForm, 'error': 'El usuario o contraseña son incorrectas'})
        else:
            login(request, user)
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
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_detail', task.id)
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_detail.html', {'task': task, 'form': form})
