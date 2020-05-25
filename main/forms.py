from django import forms
from django.core.validators import FileExtensionValidator

class UploadImageForm(forms.Form):
    image_file = forms.FileField(
        label='Choose .jpg image file of mango leaf', 
        widget=forms.FileInput(attrs={'class': 'form-control-file', 'id': 'fileUpload'}),
        validators=[FileExtensionValidator(allowed_extensions=['jpg'])])
    preprocessing = forms.BooleanField(label="Perform Preprocessing", required=False, widget=forms.CheckboxInput(attrs={'checked': '','data-toggle' : 'toggle', 'data-on':'Yes', 'data-off': 'No'}))