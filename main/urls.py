from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeFormView.as_view(), name='main.home'),
]