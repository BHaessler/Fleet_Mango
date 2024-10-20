""" Declares all of the views the pages will reach for"""

# Standard library imports
from collections import defaultdict

# Django core imports
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError  # Add this line
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from django.views.generic.edit import UpdateView

# Local application imports
from .models import Owner, VehicleType, CarMake, CarInstance, FooterContent, Feedback
from .forms import (
    UserRegisterForm,
    OwnerForm,
    UserManagementForm,
    CarInstanceForm,
    FooterContentForm,
    FeedbackForm,
    )
#--------------------------------------------------------------------------------------------------

# Views go under here
# function based views go here

def home_page(request):
    if request.user.is_authenticated:
        num_visits = increment_page_visits(request, 'home')
        num_instances = CarInstance.objects.all().count()
        num_owners = Owner.objects.all().count()

        context = {
            'num_instances': num_instances,
            'num_owners': num_owners,
            'num_visits': num_visits,
        }

        # Redirect to respective dashboards based on user group
        if request.user.groups.filter(name='Customer').exists():
            return redirect('customer_dashboard')  
        elif request.user.groups.filter(name='Admin').exists():
            return redirect('admin_dashboard')  
        elif request.user.groups.filter(name='Mechanics').exists():
            return redirect('mechanics_dashboard') 
        else:
            return render(request, 'no_auth_home.html', context)

    else:
        num_visits = increment_page_visits(request, 'no_auth_home')
        return render(request, 'no_auth_home.html', {'num_visits': num_visits})

def owner_success_view(request):
    num_visits = increment_page_visits(request, 'owner_success')
    return render(request, 'owner_success.html', {'num_visits': num_visits})

'''Implements a helper function to count the page visits'''
def increment_page_visits(request, page_name):
    session_key = f'num_visits_{page_name}'
    num_visits = request.session.get(session_key, 0)
    num_visits += 1
    request.session[session_key] = num_visits
    return num_visits


# Defining page separation by group classes here 
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return is_admin(self.request.user)

    def handle_no_permission(self):
        return redirect('unauthorized_access')


class MechanicsRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return is_mechanic(self.request.user)


class CustomerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return is_customer(self.request.user)


class IsOwnerOrAdminMixin(UserPassesTestMixin):
    def test_func(self):
        car_instance = self.get_object()
        return car_instance.owner.user == self.request.user or is_admin(self.request.user)


class IsOwnerAdminOrMechanicMixin(UserPassesTestMixin):
    def test_func(self):
        car_instance = self.get_object()
        return (
            car_instance.owner.user == self.request.user or 
            is_admin(self.request.user) or 
            is_mechanic(self.request.user)
        )

    def handle_no_permission(self):
        return redirect('unauthorized_access')


# Defining separation of users here
def login_view(request):
    num_visits = increment_page_visits(request, 'login')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.groups.filter(name='Customer').exists():
                return redirect('customer_dashboard')
            elif user.groups.filter(name='Admin').exists():
                return redirect('admin_dashboard')
            elif user.groups.filter(name='Mechanics').exists():
                return redirect('mechanic_dashboard')
            else:
                return redirect('some_other_dashboard')
    return render(request, 'login.html', {'num_visits': num_visits})


def register_view(request):
    num_visits = increment_page_visits(request, 'register')
    if request.method == "POST":
        user_form = UserRegisterForm(request.POST)
        owner_form = OwnerForm(request.POST)

        if user_form.is_valid() and owner_form.is_valid():
            user = user_form.save()

            # Check if the owner already exists for this user
            owner, created = Owner.objects.get_or_create(user=user)  # This will not create a new owner if one exists
            
            # Update the owner fields if they already exist
            if not created:
                # Optionally update existing fields if needed
                owner.first_name = owner_form.cleaned_data['first_name']
                owner.last_name = owner_form.cleaned_data['last_name']
                owner.phone_num = owner_form.cleaned_data['phone_num']
                owner.save()  # Save updates

            else:
                # If created, assign the fields from the form
                owner.first_name = owner_form.cleaned_data['first_name']
                owner.last_name = owner_form.cleaned_data['last_name']
                owner.phone_num = owner_form.cleaned_data['phone_num']
                owner.save()  # Save new owner

            return redirect('owner_success.html')  # Redirect after successful registration

    else:
        user_form = UserRegisterForm()
        owner_form = OwnerForm()
    context = {
        'user_form': user_form, 
        'owner_form': owner_form,
        'num_visits': num_visits,
    }
    return render(request, 'registration/register.html', context)


"""Admin Separation"""
def is_admin(user):
    return user.groups.filter(name='Admin').exists() # Or check for a specific group


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    # Add any admin-specific data to the context
    num_visits = increment_page_visits(request, 'admin_dashboard')
    footer_content = FooterContent.objects.first()  # Get the first (and only) footer content
    context = {
        'user': request.user,
        'num_visits': num_visits,
        'footer_content': footer_content,
        # Add other relevant data for admins
    }
    return render(request, 'dashboards/admin_dashboard.html', context)  # Ensure this matches your template path


@login_required
@user_passes_test(is_admin)
def user_list(request):
    users = User.objects.all()
    user_details = None  # Initialize to None
    num_visits = increment_page_visits(request, 'user_list')

    # Check if a user ID is passed in the request (for viewing details)
    user_id = request.GET.get('user_id')
    if user_id:
        user_details = get_object_or_404(User, pk=user_id)

    return render(request, 'user_management/user_list.html', {'users': users, 'user_details': user_details, 'num_visits': num_visits})


@login_required
@user_passes_test(is_admin)
def add_user(request):
    if request.method == "POST":
        form = UserManagementForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user first

            # Check for existing owner
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone_num = request.POST.get('phone_num')

            owner, created = Owner.objects.get_or_create(
                first_name=first_name,
                last_name=last_name,
                phone_num=phone_num,
                defaults={'user': user}
            )

            if not created:
                # If the owner already exists, you might want to update or handle it
                # For example, you can assign the user to the existing owner
                owner.user = user
                owner.save()

            return redirect('user_list')  # Redirect after saving
    else:
        form = UserManagementForm()
    return render(request, 'user_management/add_user.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def edit_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == "POST":
        form = UserManagementForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserManagementForm(instance=user)
        # Pre-populate the groups in the form
        form.fields['groups'].initial = user.groups.all()  # Set the initial groups
    return render(request, 'user_management/edit_user.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == "POST":
        user.delete()
        return redirect('user_list')
    return render(request, 'user_management/delete_user.html', {'user': user})


@login_required
@user_passes_test(is_admin)
def user_detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    num_visits = increment_page_visits(request, 'user_detail') 
    footer_content = FooterContent.objects.first()  # Fetch footer content if needed

    context = {
        'user': user,
        'num_visits': num_visits,
        'footer_content': footer_content,
    }
    return render(request, 'user_management/user_detail.html', context)

@login_required
@user_passes_test(is_admin)  
def delete_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, pk=feedback_id)
    if request.method == "POST":
        feedback.delete()
        return redirect('feedback_list')  # Redirect to the feedback list or another appropriate page
    return render(request, 'page_management/delete_feedback.html', {'feedback': feedback})


@login_required
@user_passes_test(lambda user: user.groups.filter(name='Admin').exists())
def resolve_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, pk=feedback_id)
    feedback.resolved = True
    feedback.save()
    return redirect('feedback_list')  # Redirect back to the feedback list


@login_required
@user_passes_test(lambda user: user.groups.filter(name='Admin').exists())
def feedback_list_view(request):
    users = User.objects.all()
    categories = Feedback.CATEGORY_CHOICES
    selected_user = request.GET.get('user', None)
    selected_category = request.GET.get('category', None)

    feedback_queryset = Feedback.objects.all()

    if selected_user:
        try:
            selected_user = int(selected_user)
            feedback_queryset = feedback_queryset.filter(user_id=selected_user)
        except ValueError:
            selected_user = None

    if selected_category:
        feedback_queryset = feedback_queryset.filter(category=selected_category)

    # Separate feedback into resolved and unresolved
    unresolved_feedback = feedback_queryset.filter(resolved=False)
    resolved_feedback = feedback_queryset.filter(resolved=True)

    context = {
        'unresolved_feedback': unresolved_feedback,
        'resolved_feedback': resolved_feedback,
        'users': users,
        'categories': categories,
        'selected_user': selected_user,
        'selected_category': selected_category,
    }

    return render(request, 'page_management/feedback_list.html', context)


@login_required
@user_passes_test(is_admin)  
def edit_footer_content(request):
    footer_content, created = FooterContent.objects.get_or_create(pk=1)  # Assuming only one instance is needed

    if request.method == "POST":
        form = FooterContentForm(request.POST, instance=footer_content)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # Redirect after saving
    else:
        form = FooterContentForm(instance=footer_content)

    return render(request, 'page_management/edit_footer_content.html', {'form': form})


"""Mechanics Separation"""
def is_mechanic(user):
    return user.groups.filter(name='Mechanics').exists() # Or check for a specific group


@login_required
@user_passes_test(is_mechanic)
def mechanic_dashboard(request):
    # Add any mechanic-specific data to the context
    num_visits = increment_page_visits(request, 'mechanic_dashboard')
    context = {
        'user': request.user,
        'num_visits':num_visits
        # Add other relevant data for mechanics
    }
    return render(request, 'dashboards/mechanic_dashboard.html')  # Ensure this matches your template path


def is_admin_or_mechanic(user):
    return user.groups.filter(name='Admin').exists() or user.groups.filter(name='Mechanics').exists()


"""Customer separation"""
def is_customer(user):
    return user.groups.filter(name='Customer').exists()


@login_required
@user_passes_test(is_customer)
def customer_dashboard(request):
    # Get the owner associated with the logged-in user
    owner = get_object_or_404(Owner, user=request.user)
    num_visits = increment_page_visits(request, 'customer_dashboard')
    # Fetch all cars that belong to this owner directly from the database
    customer_cars = CarInstance.objects.filter(owner=owner)

    # Add any customer-specific data to the context
    context = {
        'user': request.user,
        'owner': owner,
        'customer_cars': customer_cars,
        'num_visits':num_visits
    }
    
    return render(request, 'dashboards/customer_dashboard.html', context)


@login_required
@user_passes_test(lambda user: is_customer(user) or is_admin(user) or is_mechanic(user))
def edit_car_instance(request, car_id):
    car_instance = get_object_or_404(CarInstance, pk=car_id)
    
    # Optionally: Check if the user is the owner, admin, or mechanic
    if not (car_instance.owner.user == request.user or is_admin(request.user) or is_mechanic(request.user)):
        return redirect('unauthorized_access')  # Redirect if the user is unauthorized

    if request.method == "POST":
        form = CarInstanceForm(request.POST, instance=car_instance)
        if form.is_valid():
            form.save()  # Save the updated car instance
            return redirect('cars')  # Redirect after saving
    else:
        form = CarInstanceForm(instance=car_instance)  # Populate the form with existing data
    return render(request, 'car_management/edit_car.html', {'form': form})


@login_required
@user_passes_test(is_customer)  # Restrict to customers
def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user  # Set the user if logged in
            feedback.save()
            return redirect('feedback_success')  # Redirect after saving
    else:
        form = FeedbackForm()
    return render(request, 'page_management/feedback_form.html', {'form': form})


def feedback_success_view(request):
    return render(request, 'page_management/feedback_success.html')


# Class based views go under here
"""CAR related classes"""
class CarListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = CarInstance
    context_object_name = 'car_list'
    template_name = 'car_management/car_list.html'

    def test_func(self):
        return is_admin_or_mechanic(self.request.user)
        
    def get_queryset(self):
        return CarInstance.objects.all()  # Show all cars to admins and mechanics

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_visits'] = increment_page_visits(self.request, 'cars')
        return context


class CarDetailView(LoginRequiredMixin, IsOwnerAdminOrMechanicMixin, DetailView):
    model = CarInstance
    template_name = 'car_management/car_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_visits'] = increment_page_visits(self.request, f'car_detail_{self.object.pk}')
        return context


"""OWNER related classes"""
class OwnerListView(UserPassesTestMixin, ListView):
    model = Owner
    context_object_name = 'owner_list'
    template_name = 'owner_management/owner_list.html'
    
    def test_func(self):
        return is_admin(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_visits'] = increment_page_visits(self.request, 'owner_list')
        return context


class OwnerDetailView(DetailView):
    model = Owner
    template_name = 'owner_management/owner_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_visits'] = increment_page_visits(self.request, f'owner_detail_{self.object.pk}')
        return context


class OwnerCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Owner
    form_class = OwnerForm
    template_name = 'owner_management/owner_details.html'
    
    def test_func(self):
        return is_admin(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_visits'] = increment_page_visits(self.request, 'owner_create')
        return context

    def get_success_url(self):
        return reverse('owner-success')  # Use the name of your success URL pattern
    
    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        # Handle invalid form submission (e.g., return to the same page with errors)
        return super().form_invalid(form)


class OwnerEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Owner
    form_class = OwnerForm
    template_name = "owner_management/owner_edit.html"

    def test_func(self):
        owner = self.get_object()
        return is_admin(self.request.user) or owner.user == self.request.user

    def get_success_url(self):
        return reverse('owner-detail', args=[self.object.pk])


"""CUSTOMER related classes"""
class CustomerCarListView(LoginRequiredMixin, CustomerRequiredMixin, ListView):
    model = CarInstance
    template_name = 'car_management/customer_car_list.html'
    context_object_name = 'customer_cars'

    def get_queryset(self):
        return CarInstance.objects.filter(owner__user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_visits'] = increment_page_visits(self.request, 'customer_car_list')
        return context