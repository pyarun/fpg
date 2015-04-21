from rest_framework import viewsets
from facility.models import Club, Resource, Booking
from facility.serializers import ClubSerializer, ResourceSerializer, BookingSerializer


class ClubView(viewsets.ModelViewSet):
    '''
        Club to create, update, delete and list the clubs
    '''

    model = Club
    serializer_class = ClubSerializer
    queryset = Club.objects.all()

class ResourceView(viewsets.ModelViewSet):
    '''
        To list, create, update, delete resources.
    '''

    model = Resource
    serializer_class =  ResourceSerializer
    queryset = Resource.objects.all()


class BookingView(viewsets.ModelViewSet):
    '''
        To list, create, update, delete resources.
    '''
    model = Booking
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()