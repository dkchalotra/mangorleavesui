from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeFormView.as_view(), name='main.home'),
    path('leaf/<int:pk>/', views.LeafDetailView.as_view(), name='leaf.detail'),
    path('leaves/', views.LeafListView.as_view(), name='leaf.list'),
]