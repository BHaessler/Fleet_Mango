""" Declares urls for the web app to use and reference"""

from django.urls import path
from . import views

from .views import OwnerCreateView, owner_success_view 

# URL Patterns fall under here
urlpatterns = [
    path('', views.home_page, name='index'), #homepage path

    #CAR oriented paths go here
    path('cars/', views.CarListView.as_view(), name='cars'),
    path('car/<int:pk>/', views.CarDetailView.as_view(), name='car-detail'),

    #OWNER oriented paths go here
    path('owner/create/', OwnerCreateView.as_view(), name='owner-create'),
    path('owner/success/', owner_success_view, name='owner-success'),  # Success URL
    path('owner/<int:pk>/', views.OwnerDetailView.as_view(), name='owner-detail'),
    path('owners/', views.OwnerListView.as_view(), name='owners'),
    
    #Separational View paths go here
    path('customer/', views.customer_dashboard, name='customer_dashboard'),
    path('customer/cars/', views.CustomerCarListView.as_view(), name='customer_cars'),
    ]
