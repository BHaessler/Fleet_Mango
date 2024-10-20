""" Declares urls for the web app to use and reference"""

from django.urls import path
from . import views

from .views import (
    OwnerCreateView, 
    OwnerEditView,
    CarListView,
    CustomerCarListView,
    owner_success_view, 
    register_view, 
    edit_footer_content,
    user_list, 
    add_user, 
    edit_user, 
    delete_user, 
    feedback_view, 
    feedback_list_view, 
    feedback_success_view, 
    delete_feedback, 
    resolve_feedback
)

# URL Patterns fall under here
urlpatterns = [
    path('', views.home_page, name='index'), #homepage path

    path('edit-footer/', edit_footer_content, name='edit_footer_content'), #edit footer content

    # feedback oriented paths go here
    path('feedback/', feedback_view, name='feedback'),
    path('feedback/success/', feedback_success_view, name='feedback_success'),
    path('feedback/delete/<int:feedback_id>/', delete_feedback, name='delete_feedback'),
    path('feedback/resolve/<int:feedback_id>/', resolve_feedback, name='resolve_feedback'),

    #CAR oriented paths go here
    path('cars/', CarListView.as_view(), name='cars'),
    path('my-cars/', CustomerCarListView.as_view(), name='customer_car_list'),
    path('car/<int:pk>/', views.CarDetailView.as_view(), name='car-detail'),
    path('car/edit/<int:car_id>/', views.edit_car_instance, name='edit_car_instance'),

    #OWNER oriented paths go here
    path('owner/create/', OwnerCreateView.as_view(), name='owner-create'),
    path('owner/success/', owner_success_view, name='owner-success'),  # Success URL
    path('owner/<int:pk>/', views.OwnerDetailView.as_view(), name='owner-detail'),
    path('owner/edit/<int:pk>/', OwnerEditView.as_view(), name='edit_owner'),
    path('owners/', views.OwnerListView.as_view(), name='owners'),
    
    #Separational View paths go here
    path('register/', register_view, name='register'),

    #Customer paths go here
    path('customer/', views.customer_dashboard, name='customer_dashboard'),
    path('customer/cars/', views.CustomerCarListView.as_view(), name='customer_cars'),

    # Admin Paths go here
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/feedback/', feedback_list_view, name='feedback_list'),

    # Mechanics Paths go here
    path('mechanics/dashboard/', views.mechanic_dashboard, name='mechanics_dashboard'),

    # User Management Paths go here
    path('users/', user_list, name='user_list'),
    path('users/add/', add_user, name='add_user'),
    path('users/edit/<int:user_id>/', edit_user, name='edit_user'),
    path('users/delete/<int:user_id>/', delete_user, name='delete_user'),
    
    ]
