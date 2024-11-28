from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    datecompleted = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Fecha de finalización',
        required=False
    )

    class Meta:
        model = Task
        fields = [
            'companyname', 
            'workreason', 
            'description', 
            'payment', 
            'datecompleted', 
            'important', 
            'payment_pdf', 
            'payment_image', 
            'payment_xml'
        ]
        labels = {
            'companyname': 'Nombre de la empresa',
            'workreason': 'Razón del trabajo',
            'description': 'Descripción',
            'payment': 'Pago acordado',
            'datecompleted': 'Fecha de finalización',
            'important': 'Importante',
            'payment_pdf': 'Archivo PDF del pago',
            'payment_image': 'Imagen del pago',
            'payment_xml': 'Archivo XML del pago',
        }

    # Campo solo de lectura para la fecha de creación NO FUNCIOONO
    #created = forms.DateTimeField(label='Fecha de creación', required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
