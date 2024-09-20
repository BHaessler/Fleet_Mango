from django.shortcuts import render
# Everything under here I added
from .models import Owner, VehicleType, CarMake, CarInstance
from django.views import generic
# Create your views here.

def index(request):
    """View function for the homepage of the site"""

    # Generate counts of some of the main objects
    num_cars = CarMake.objects.all().count()
    num_instances = CarInstance.objects.all().count()

    num_owners = Owner.objects.all().count()


    context = {
        'num_cars': num_cars,
        'num_instances': num_instances,

        'num_owners': num_owners,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class CarListView(generic.ListView):
    model = CarInstance
    context_object_name = 'car_list'
    paginate_by = 10

class CarDetailView(generic.DetailView):
    model = CarMake