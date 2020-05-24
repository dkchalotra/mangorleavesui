from django import forms
from django.core.validators import FileExtensionValidator

class UploadImageForm(forms.Form):
    image_file = forms.FileField(
        label='Upload a picture of Mango Leaf', 
        widget=forms.FileInput(attrs={'class': 'form-control-file', 'id': 'fileUpload'}),
        validators=[FileExtensionValidator(allowed_extensions=['jpg'])])