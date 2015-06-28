import datetime
from rest_framework import viewsets, filters

from facility.models import Club, Resource, Booking
from facility.serializers import ClubSerializer, ResourceSerializer, BookingSerializer, SlotSerializer
from rest_framework.viewsets import GenericViewSet

class ClubView(viewsets.ModelViewSet):
    """
        Create update delete and list the clubs
    """
    model = Club
    serializer_class = ClubSerializer
    queryset = Club.objects.all()
    filter_fields = ('id' ,'owner', 'address')
    filter_backends = viewsets.ModelViewSet.filter_backends


class ResourceView(viewsets.ModelViewSet):
    """
        To list, create, update, delete resources.
    """
    model = Resource
    serializer_class = ResourceSerializer
    queryset = Resource.objects.all()
    filter_fields = ('id' ,'club', 'sport')
    filter_backends = viewsets.ModelViewSet.filter_backends

    def get_queryset(self):
        """
         Modify default get_queryset method to filter address
        """
        queryset = super(ResourceView, self).get_queryset()
        address = self.request.query_params.get('address', None)
        date = self.request.query_params.get('date', None)
        start_time = self.request.query_params.get('start_time', None)
        end_time = self.request.query_params.get('end_time', None)
        # import ipdb;ipdb.set_trace()
        if date:
            date =  datetime.datetime.strptime(date, '%m/%d/%Y').strftime('%Y-%m-%d')

        # import ipdb; ipdb.set_trace()
        if address is not None:
            queryset = queryset.filter(club__address=address)

        if date is not None:
            resource_ids = Booking.objects.exclude(date=date).values_list('resource')
            queryset = queryset.filter(id__in = resource_ids)
            resource_ids = [item[0] for item in resource_ids]
            queryset = queryset.filter(id__in = resource_ids)
            # import ipdb; ipdb.set_trace()

        if start_time and end_time:
            resource_id = Booking.objects.exclude(start_time__gte = start_time, end_time__lte = end_time).values_list('resource_id')
            # import ipdb; ipdb.set_trace()
            resource_id = [item[0] for item in resource_id]
            queryset = queryset.filter(id__in = resource_id)
        return queryset


class BookingView(viewsets.ModelViewSet):
    """
        To list, create, update, delete bookings
    """
    model = Booking
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()
    filter_fields = ('id' ,'date')
    filter_backends = viewsets.ModelViewSet.filter_backends

    def get_queryset(self):
        """
         Modify default get_queryset method to filter
        """
        queryset = super(BookingView, self).get_queryset()
        date = self.request.query_params.get('date', None)
        # start_time = self.request.query_params.get('start_time', None)
        # end_time = self.request.query_params.get('end_time', None)
        # import ipdb;ipdb.set_trace()
        if date:
            date =  datetime.datetime.strptime(date, '%m/%d/%Y').strftime('%Y-%m-%d')


        if date is not None:
            resource_ids = Booking.objects.filter(date=date).values_list('resource')
            queryset = queryset.filter(id__in = resource_ids)
            resource_ids = [item[0] for item in resource_ids]
            queryset = queryset.filter(id__in = resource_ids)

        # if start_time and end_time:
        #     resource_id = Booking.objects.exclude(start_time__gte = start_time, end_time__lte = end_time).values_list('resource_id')
        #     # import ipdb; ipdb.set_trace()
        #     resource_id = [item[0] for item in resource_id]
        #     queryset = queryset.filter(id__in = resource_id)

        return queryset



class SlotView(viewsets.ModelViewSet):
    """

    """
    model = Booking
    serializer_class = SlotSerializer
    queryset = Booking.objects.all()


