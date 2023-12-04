from django.db import models


class UploadedFile(models.Model):
    csv_file = models.FileField(upload_to='uploads/')

