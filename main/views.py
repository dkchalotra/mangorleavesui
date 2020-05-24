from django.views.generic import FormView
from django.urls import reverse_lazy
from django.conf import settings
from . import forms
import string
import random
import os

# Create your views here.
class HomeFormView(FormView):
    form_class = forms.UploadImageForm
    template_name = 'main/main.html'
    success_url = reverse_lazy('main.home')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('image_file')
        if form.is_valid():
            self.save_upload_file(files[0])
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def save_upload_file(self, file):
        file_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=64)) + "." + file.name.split('.')[-1]
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)