""" Declares urls for the web app to use and reference"""

from django.urls import path
from . import views

from .views import OwnerCreateView, owner_success_view 

# URL Patterns fall under here
urlpatterns = [
    path('', views.index, name='index'),
    path('cars/', views.CarListView.as_view(), name='cars'),
    path('car/<int:pk>/', views.CarDetailView.as_view(), name='car-detail'),

    path('owner/create/', OwnerCreateView.as_view(), name='owner-create'),
    path('owner/success/', owner_success_view, name='owner-success'),  # Success URL
    path('owner/<int:pk>/', views.OwnerDetailView.as_view(), name='owner-detail'),
    path('owners/', views.OwnerListView.as_view(), name='owners'),
    
    ]
