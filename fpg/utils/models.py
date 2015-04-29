from django.db import models

class Sports(models.Model):
    '''
        Game model for perticular game for which user will be booking slot
    '''
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=400, null=True, blank=True)

    def __unicode__(self):
        return self.name


class Address(models.Model):
    """
        Address table with address fields
        primary key of this is used in UserProfile, Farm, GrocerShop
    """
    lane1 = models.CharField(max_length=100)
    lane2 = models.CharField(max_length=100, null=True, blank=True)
    area = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __unicode__(self):
        return self.city
