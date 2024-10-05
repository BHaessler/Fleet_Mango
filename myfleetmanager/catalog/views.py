""" Declares all of the views the pages will reach for"""

from django.shortcuts import render, redirect
# Everything under here I added
from .models import Owner, VehicleType, CarMake, CarInstance
from django.views import generic
from django.views.generic import ListView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from .forms import OwnerForm  # the form is named owner form

# Views go under here
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
        return render(request, 'index.html', context=context)
    else:
        num_visits = increment_page_visits(request, 'no_auth_home')
        return render(request, 'no_auth_home.html', {'num_visits': num_visits})


def owner_success_view(request):
    num_visits = increment_page_visits(request, 'owner_success')
    return render(request, 'owner_success.html', {'num_visits': num_visits})

'''implements a helper function to count the page visits'''
def increment_page_visits(request, page_name):
    session_key = f'num_visits_{page_name}'
    num_visits = request.session.get(session_key, 0)
    num_visits += 1
    request.session[session_key] = num_visits
    return num_visits


# Classes go under here
"""CAR related classes"""
class CarListView(ListView):
    model = CarInstance
    context_object_name = 'car_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_visits'] = increment_page_visits(self.request, 'car_list')
        return context

class CarDetailView(DetailView):
    model = CarInstance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_visits'] = increment_page_visits(self.request, f'car_detail_{self.object.pk}')
        return context

"""OWNER related classes"""
class OwnerListView(ListView):
    model = Owner
    context_object_name = 'owner_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_visits'] = increment_page_visits(self.request, 'owner_list')
        return context

class OwnerDetailView(DetailView):
    model = Owner
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_visits'] = increment_page_visits(self.request, f'owner_detail_{self.object.pk}')
        return context

class OwnerCreateView(CreateView):
    model = Owner
    form_class = OwnerForm
    template_name = 'Owner_details.html'

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
