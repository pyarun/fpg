from rest_framework import viewsets, filters

from facility.models import Club, Resource, Booking
from facility.serializers import ClubSerializer, ResourceSerializer, BookingSerializer
from rest_framework.viewsets import GenericViewSet

class ClubView(viewsets.ModelViewSet):
    """
        Create update delete and list the clubs
    """
    model = Club
    serializer_class = ClubSerializer
    # queryset = Club.objects.all()
    filter_fields = ('id' ,'owner')
    filter_backends = viewsets.ModelViewSet.filter_backends

    def get_queryset(self):
        return Club.objects.all()

class ResourceView(viewsets.ModelViewSet):
    """
        To list, create, update, delete resources.
    """
    model = Resource
    serializer_class = ResourceSerializer
    queryset = Resource.objects.all()
    filter_fields = ('id' ,'club')
    filter_backends = viewsets.ModelViewSet.filter_backends


class BookingView(viewsets.ModelViewSet):
    """
        To list, create, update, delete bookings
    """
    model = Booking
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()