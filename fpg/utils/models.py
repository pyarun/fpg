# Create your models here.

# class Address(models.Model):
# """
# Address table with address fields
#         primary key of this is used in UserProfile, Farm, GrocerShop
#     """
#     lane1 = models.CharField(max_length=100)
#     lane2 = models.CharField(max_length=100, null=True, blank=True)
#     area = models.CharField(max_length=100, null=True, blank=True)  #
#     city = models.CharField(max_length=100)
#     state = models.CharField(max_length=100)
#     country = models.CharField(max_length=100)
#
#     def __unicode__(self):
#         return self.city
