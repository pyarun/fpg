from address.models import Address
from django.contrib.auth.models import User
from django.db import models

from utils.models import Sports


class Club(models.Model):
    '''
        Club model with basic fields
    '''
    name = models.CharField(max_length=100)
    owner = models.OneToOneField(User, null=True, blank=True)
    address = models.OneToOneField(Address, null=True, blank=True)
    contact_number = models.CharField(max_length=12, null=True, blank=True)
    description = models.CharField(max_length=400, null=True, blank=True)

    def __unicode__(self):
        return self.name


class Resource(models.Model):
    '''
        Turf model of a particular club and sport
    '''
    STATUS = (('available', 'Available'), ('unavailable', 'Unavailable'))

    name = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    club = models.ForeignKey(Club)
    open_time = models.TimeField(null=True, blank=True)
    close_time = models.TimeField(null=True, blank=True)
    fees = models.PositiveIntegerField()
    sport = models.ForeignKey(Sports)
    photo = models.ImageField(upload_to='resources')
    status = models.CharField(choices=STATUS, max_length=32, default=STATUS[0][0])
    description = models.CharField(max_length=400, null=True, blank=True)

    def __unicode__(self):
        return self.name


class Booking(models.Model):
    '''
        Booking model for booking resources which user will book
    '''
    title = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    resource = models.ForeignKey(Resource)