from django.db import models
# Everything below here I have added
from django.urls import reverse # Used in get_absolute_url() to get URL for specified ID

from django.db.models import UniqueConstraint # Constrains fields to unique values
from django.db.models.functions import Lower # Returns lower cased value of field
from django.conf import settings

# Direct imports are here
from datetime import date

# Create your models below here.
class VehicleType(models.Model):
    """Model representing a type or class of vehicle."""
    name = models.CharField(
        max_length=20,
        unique=True,
        help_text="Enter a vehicle class (e.g. SUV, Sedan, Minivan, etc.)"
    )

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a particular vehicle type instance."""
        return reverse('vehicle-class-detail', args=[str(self.id)])


class CarMake(models.Model):
    """Model representing a make of a car (but not a specific car)."""
    manuName = models.CharField(max_length=20)
    
    carModel = models.CharField(
        max_length=100, help_text="Enter a brief description of the Car(IE: Model)")
    
    # ForeignKey used because type can contain many cars. Cars can't cover many types.
    # VehicleType class has already been defined so we can specify the object above.
    vehicleType = models.ForeignKey(VehicleType, help_text="Select a vehicle type for this car", on_delete=models.RESTRICT, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.manuName

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this manufacturer."""
        return reverse('car-make-detail', args=[str(self.id)])


class CarInstance(models.Model):
    """Model representing a specific car in the shop"""
    car = models.ForeignKey('CarMake', on_delete=models.RESTRICT, null=True)
    owner = models.ForeignKey('Owner', on_delete=models.RESTRICT, null=True)
    # Foreign Key used because car can only have one owner, but owners can have multiple cars.
    # Owner as a string rather than object because it hasn't been declared yet in file.

    vinNum = models.CharField(max_length=17, help_text="Unique VIN for this particular vehicle in the garage")
    
    modelYear = models.CharField(max_length=4, help_text="What year is this model?")
    color = models.CharField(max_length=50, help_text="What is the common name of the vehicle's color and also its paint code.")
    license_plate = models.CharField(max_length=12, help_text="What is the plate for this vehicle")
    due_back = models.DateField(null=True, blank=True)
    
    mechanic_stat = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    CAR_STATUS = (
        ('M', 'Maintenance'),
        ('O', 'Owner has vehicle in their possession'),
        ('S', 'Scrap or Parts vehicle'),
        ('A', 'Available'),
        ('R', 'Ready for release to owner'),
    )

    status = models.CharField(
        max_length=1,
        choices=CAR_STATUS,
        blank=True,
        default='A',
        help_text='Car Status',
    )
    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.license_plate} ({self.car.manuName})'

    def get_absolute_url(self):
        """Returns the url to access a particular car record."""
        return reverse('car-detail', args=[str(self.id)])

    @property
    def is_overdue(self):
        """Determines if the book is overdue based on due date and current date."""
        return bool(self.due_back and date.today() > self.due_back)


class Owner(models.Model):
    """Model representing an owner."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('owner-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'