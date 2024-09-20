from django.shortcuts import render
# Everything under here I added
from .models import Owner, VehicleType, CarMake, CarInstance
from django.views import generic
# Create your views here.

def index(request):
    """View function for the homepage of the site"""

    # Generate counts of some of the main objects
    num_instances = CarInstance.objects.all().count()
    num_owners = Owner.objects.all().count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    num_visits += 1
    request.session['num_visits'] = num_visits


    context = {
        'num_instances': num_instances,
        'num_owners': num_owners,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class CarListView(generic.ListView):
    model = CarInstance

class CarDetailView(generic.DetailView):
    model = CarInstance