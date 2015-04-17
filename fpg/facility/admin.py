from django.contrib import admin

# Register your models here.
from facility.models import Resource, Booking, Club
from profiles.models import UserProfile
from utils.models import Sports

admin.site.register(UserProfile, admin.ModelAdmin)
admin.site.register(Resource, admin.ModelAdmin)
admin.site.register(Booking, admin.ModelAdmin)
admin.site.register(Club, admin.ModelAdmin)
admin.site.register(Sports, admin.ModelAdmin)