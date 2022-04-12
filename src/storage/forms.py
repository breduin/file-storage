from django import forms
from .models import FileUpload


class UploadFileForm(forms.Form):

    description = forms.CharField(
        max_length=128,
        required=False
        )
    uploaded_file = forms.FileField()
