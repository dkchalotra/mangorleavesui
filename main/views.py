from django.views.generic import FormView
from django.urls import reverse
from django.conf import settings
from . import forms
from . import models
import string
import random
import numpy
import os
import joblib
from .feature_extraction import extract_features
from .preprocessing import preprocess_image

labels_map = {
    0: models.LeafModel.ALPHONSO,
    1: models.LeafModel.AMRAPALI,
    2: models.LeafModel.CHAUNSA,
    3: models.LeafModel.DUSHERI,
    4: models.LeafModel.LANGRA,
}

RECENT_CLASSIFICATIONS_COUNT = 8

# Create your views here.
class HomeFormView(FormView):
    form_class = forms.UploadImageForm
    template_name = 'main/main.html'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            files = request.FILES.getlist('image_file')
            file_save_path = self.save_upload_file(files[0])
            # preprocess image
            do_preprocessing = form.cleaned_data.get('preprocessing')
            if do_preprocessing:
                preprocess_image(file_save_path)
            # classify image file
            leaf_label = self.classify_image(file_save_path)
            new_leaf = models.LeafModel(image_file=os.path.basename(file_save_path), variety=leaf_label)
            new_leaf.save()
            self.success_url = reverse('main.home') + "?prediction=" + leaf_label
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
        return file_path
    
    def classify_image(self, img_path):
        features = extract_features(img_path)
        svm_classifier = joblib.load(settings.SVM_CLASSIFIER_PATH)
        X = numpy.array([[
            features.aspectratio,
            features.area,
            features.perimeter,
            features.formfactor,
            features.meancolor[0],
            features.meancolor[1],
            features.meancolor[2],
            features.veinarea1,
            features.veinarea2,
            features.elongation,
        ]], dtype=float)
        Y = labels_map[svm_classifier.predict(X)[0]]
        return Y

    def get_context_data(self, **kwargs):
        data =  super().get_context_data(**kwargs)
        # Add recent leaves classifications
        recent_leaves = models.LeafModel.objects.order_by('-id')[:RECENT_CLASSIFICATIONS_COUNT].all()
        data['recent_leaves'] = recent_leaves
        return data