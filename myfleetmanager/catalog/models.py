"""Models for the catalog application."""

from django.db import models
# Everything below here I have added
from django.urls import reverse # Used in get_absolute_url() to get URL for specified ID
from django.db.models.functions import Lower # Returns lower cased value of field
from django.conf import settings
from django.contrib.auth.models import User  # Add this line to import User

# Direct imports are here
from datetime import date

# Create your models below here.
"""Model representing a type or class of vehicle."""
class VehicleType(models.Model):
    
    name = models.CharField(
        max_length=20,
        unique=True,
        help_text="Enter a vehicle class (e.g. SUV, Sedan, Minivan, etc.) This will categorize your vehicles."
    )

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a particular vehicle type instance."""
        return reverse('vehicle-class-detail', args=[str(self.id)])

"""Model representing a make of a car (but not a specific car)."""
class CarMake(models.Model):
    manuName = models.CharField(max_length=20, help_text="Enter the name of the car manufacturer (e.g., Toyota, Ford).")
    
    carModel = models.CharField(
        max_length=100, help_text="Enter the car model (e.g., Camry, F-150)."
    )
    
    vehicleType = models.ForeignKey(
        VehicleType,
        help_text="Select the type of vehicle this car belongs to (e.g., SUV, Sedan).",
        on_delete=models.RESTRICT,
        null=True
    )

    def __str__(self):
        """String for representing the Model object."""
        return self.manuName

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this manufacturer."""
        return reverse('car-make-detail', args=[str(self.id)])

"""Model representing a specific car in the shop"""
class CarInstance(models.Model):
    
    car = models.ForeignKey('CarMake', on_delete=models.RESTRICT, null=True)
    owner = models.ForeignKey('Owner', on_delete=models.RESTRICT, null=True)
    # Foreign Key used because car can only have one owner, but owners can have multiple cars.
    # Owner as a string rather than object because it hasn't been declared yet in file.
    vinNum = models.CharField(
        max_length=17, blank=True, null=True,
        help_text="Enter the Vehicle Identification Number (VIN) for this vehicle. It must be exactly 17 characters."
    )
    
    modelYear = models.CharField(
        max_length=4,
        help_text="Enter the year this car model was manufactured (e.g., 2020)."
    )
    
    color = models.CharField(
        max_length=50,
        help_text="Enter the common name of the vehicle's color (e.g., Red) and its paint code."
    )
    
    license_plate = models.CharField(
        max_length=12,
        help_text="Enter the vehicle's license plate number. Maximum length is 12 characters."
    )
    
    due_back = models.DateField(
        null=True,
        blank=True,
        help_text="Enter the date by which the vehicle should be returned. Leave blank if not applicable."
    )
    
    mechanic_stat = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Select the mechanic assigned to this vehicle, if applicable."
    )
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
        help_text="Select the current status of the car: M (Maintenance), O (Owner has vehicle), S (Scrap), A (Available), R (Ready for release)."
    )

    class Meta:
        """Model representing a ordering method"""
        ordering = ['due_back']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.license_plate} ({self.car.manuName})'

    def get_absolute_url(self):
        """Returns the url to access a particular car record."""
        return reverse('car-detail', args=[str(self.id)])

    @property
    def is_overdue(self):
        """Determines if the car is overdue based on due date and current date."""
        return bool(self.due_back and date.today() > self.due_back)

"""Model representing an owner."""
class Owner(models.Model):
    #The line below allows the owners to login and see their version of the site
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(
        max_length=100,
        help_text="Enter the owner's first name."
    )
    
    last_name = models.CharField(
        max_length=100,
        help_text="Enter the owner's last name."
    )
    
    phone_num = models.CharField(
        max_length=10,
        help_text="Enter the owner's phone number (e.g., 1234567890). Maximum 10 digits."
    )
    
    address = models.TextField(
        max_length=300,
        help_text="Enter the owner's address. This can be a full street address."
    )
    
    has_insurance = models.BooleanField(
        default=False,
        help_text="Check if the owner has insurance for their vehicle."
    )
    
    insurance_provider = models.CharField(
        max_length=100,
        blank=True,
        default='Unknown',
        help_text="Enter the name of the insurance provider (if applicable)."
    )
    
    insurance_policy_number = models.CharField(
        max_length=50,
        blank=True,
        default='Unknown',
        help_text="Enter the insurance policy number (if applicable)."
    )

    def clean(self):
        """Custom validation to ensure the phone number is valid."""
        if not self.phone_num.isdigit():
            raise ValidationError('Phone number must contain only digits.')
        if len(self.phone_num) < 10:
            raise ValidationError('Phone number must be at least 10 digits long.')

    class Meta: #orders the owners in the system as well as prevents duplicates 
        ordering = ['last_name', 'first_name']
        unique_together = ['first_name', 'last_name', 'phone_num']

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('owner-detail', args=[str(self.id)])

    def full_name(self): #provides a pretty print of the owners Name
        return f"{self.first_name} {self.last_name}"

    def __str__(self): # provides a last name first of the owners Name
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'

class FooterContent(models.Model):
    about_us = models.TextField(
        help_text="Enter a brief description of your company or website to display in the footer."
    )
    
    contact_email = models.EmailField(
        help_text="Enter the contact email address that users can reach out to."
    )
    
    contact_phone = models.CharField(
        max_length=15,
        help_text="Enter the contact phone number for customer inquiries."
    )
    def __str__(self):
        return "Footer Content"

class Feedback(models.Model):
    CATEGORY_CHOICES = [
        ('site', 'Site Feedback'),
        ('personnel', 'Personnel Feedback'),
        ('shop', 'Shop Feedback'),
        ('general', 'General Feedback'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField(
        help_text="Enter your feedback or comments here."
    )
    
    category = models.CharField(
        max_length=10,
        choices=CATEGORY_CHOICES,
        default='general',
        help_text="Select the category that best describes your feedback.")

    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Feedback from {self.user.username if self.user else "Anonymous"}'
# There should always be a trailing white space in these files 
