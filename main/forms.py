from django import forms

class UploadImageForm(forms.Form):
    image_file = forms.FileField(label='Upload a picture of Mango Leaf', widget=forms.FileInput(attrs={'class': 'form-control-file', 'id': 'fileUpload'}))