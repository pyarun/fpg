from django.db import models
from django.contrib.auth.models import User

from address.models import Address


class UserProfile(models.Model):
    """
        User profile table with common user fields.
    """
    user = models.OneToOneField(User)
    contact_number = models.CharField(max_length=12, null=True, blank=True)
    address = models.OneToOneField(Address, null=True, blank=True)
    about_me = models.CharField(max_length=400, null=True, blank=True)
