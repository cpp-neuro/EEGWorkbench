from django.db import models
import os

from EEGWorkbench.settings import BASE_DIR

UPLOAD_DIR = os.path.join(BASE_DIR, "workbench/uploaded_files")


class UploadedFile(models.Model):
    file = models.FileField(upload_to="uploaded_files")
