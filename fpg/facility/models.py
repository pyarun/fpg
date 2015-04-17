from address.models import Address
from django.contrib.auth.models import User
from django.db import models

from utils.models import Sports


class Club(models.Model):
    '''
        Academy or institute which provide facility or playgrounds
    '''
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, help_text='Owner of the club')
    address = models.OneToOneField(Address)
    contact_number = models.CharField(max_length=12)
    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class Resource(models.Model):
    '''
        Playground or the equipment that are provided by clubs
    '''
    STATUS = (('available', 'Available'), ('unavailable', 'Unavailable'))

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100, null=True, blank=True,
                            help_text='Type of ground or resource')
    club = models.ForeignKey(Club)
    open_time = models.TimeField(help_text='Time from which resource is available')
    close_time = models.TimeField(help_text='Time up to resource is available')
    fee = models.PositiveIntegerField(help_text='Cost of the resource per hour')
    sport = models.ForeignKey(Sports)
    photo = models.ImageField(upload_to='resources', null=True, blank=True)
    status = models.CharField(choices=STATUS, max_length=32, default=STATUS[0][0],
                              help_text='Status of resource whether it is available for booking or not')
    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class Booking(models.Model):
    '''
        Booking model for booking resources which user will book
    '''
    user = models.ForeignKey(User)
    title = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateField(help_text='Booking date')
    start_time = models.TimeField(help_text='start time of booking')
    end_time = models.TimeField(help_text='end time of booking')
    resource = models.ForeignKey(Resource)