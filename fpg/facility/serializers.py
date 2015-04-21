from rest_framework import serializers
from facility.models import Club, Resource, Booking

from profiles.serializers import AddressSerializer


class ClubSerializer(serializers.ModelSerializer):
    '''
        User can create, update, list and delete Clubs
    '''
    address = AddressSerializer()

    class Meta:
        model = Club
        fields = ('id','name','owner','address', 'contact_number', 'description')


class ResourceSerializer(serializers.ModelSerializer):
    '''
        For create, update, delete, list resources.
    '''

    class Meta:
        model = Resource
        fields = ('id', 'name', 'type', 'club', 'open_time', 'close_time', 'fee', 'sport', 'photo',
                  'status', 'description')


class BookingSerializer(serializers.ModelSerializer):
    '''
        For create, update, list, delete bookings
    '''
    class Meta:
        model = Booking
        fields = ('id', 'user', 'title', 'date', 'start_time', 'end_time', 'resource')
