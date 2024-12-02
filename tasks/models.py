from django.db import models
from django.contrib.auth.models import User
import os

class Task(models.Model):
    companyname = models.CharField(max_length=100)
    workreason = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    payment = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    completed_by = models.ForeignKey(User, related_name='tasks_completed', on_delete=models.SET_NULL, null=True, blank=True)

    payment_pdf = models.FileField(upload_to='payments/pdfs/', null=True, blank=True)
    payment_image = models.ImageField(upload_to='payments/images/', null=True, blank=True)
    payment_xml = models.FileField(upload_to='payments/xmls/', null=True, blank=True)

    def __str__(self):
        return self.companyname + '- registrado por ' + self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Guarda la tarea sin hacer nada extra.



