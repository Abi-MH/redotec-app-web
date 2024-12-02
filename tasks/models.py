from django.db import models
from django.contrib.auth.models import User
import os
from .google_drive_utils import upload_to_drive  # Asegúrate de que esta función esté importada correctamente.

class Task(models.Model):
    # Campos de la tabla
    companyname = models.CharField(max_length=100)
    workreason = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    payment = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    completed_by = models.ForeignKey(User, related_name='tasks_completed', on_delete=models.SET_NULL, null=True, blank=True)

    # Campos adicionales para archivos
    payment_pdf = models.FileField(upload_to='payments/pdfs/', null=True, blank=True)
    payment_image = models.ImageField(upload_to='payments/images/', null=True, blank=True)
    payment_xml = models.FileField(upload_to='payments/xmls/', null=True, blank=True)

    def __str__(self):
        return self.companyname + '- registrado por ' + self.user.username

    def save(self, *args, **kwargs):
        # Sobrescribe archivos antiguos si se reemplazan
        try:
            old_task = Task.objects.get(pk=self.pk)
            if old_task.payment_pdf != self.payment_pdf and old_task.payment_pdf:
                old_task.payment_pdf.delete(save=False)
            if old_task.payment_image != self.payment_image and old_task.payment_image:
                old_task.payment_image.delete(save=False)
            if old_task.payment_xml != self.payment_xml and old_task.payment_xml:
                old_task.payment_xml.delete(save=False)
        except Task.DoesNotExist:
            pass

        # Subir archivos a Google Drive y luego eliminar los archivos locales
        if self.payment_pdf:
            file_id_pdf = upload_to_drive(self.payment_pdf.path, self.payment_pdf.name)
            self.payment_pdf = None  # Elimina el archivo local después de subirlo

        if self.payment_image:
            file_id_image = upload_to_drive(self.payment_image.path, self.payment_image.name)
            self.payment_image = None  # Elimina el archivo local después de subirlo

        if self.payment_xml:
            file_id_xml = upload_to_drive(self.payment_xml.path, self.payment_xml.name)
            self.payment_xml = None  # Elimina el archivo local después de subirlo

        super().save(*args, **kwargs)
