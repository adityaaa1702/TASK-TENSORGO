from django import forms
from .models import UploadedFile
import pandas as pd

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['csv_file']
        
   