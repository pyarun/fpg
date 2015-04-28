# from address.models import AddressField, Address

from django.db import models
from django.contrib.auth.models import User
from utils.models import Address


class UserProfile(models.Model):
    """
        User profile table with common user fields.
    """
    user = models.OneToOneField(User, related_name="profile")
    contact_number = models.CharField(max_length=12, null=True, blank=True)
    address = models.OneToOneField(Address, null=True, blank=True)
    # address = AddressField(blank=True, null=True)
    about_me = models.CharField(max_length=400, null=True, blank=True)

    def __unicode__(self):
        return self.user.get_full_name()

