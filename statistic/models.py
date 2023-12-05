from django.db import models
import os


class UploadedFile(models.Model):
    csv_file = models.FileField(upload_to='uploads/')
    

