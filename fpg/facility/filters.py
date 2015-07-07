import datetime

from rest_framework.filters import BaseFilterBackend
from facility.models import Booking


class ResourceFilter(BaseFilterBackend):
    """
    Returns queryset containing
    """
    def filter_queryset(self, request, queryset, view):
        address = request.query_params.get('address', None)
        date = request.query_params.get('date', None)
        start_time = request.query_params.get('start_time', None)
        end_time = request.query_params.get('end_time', None)
        if date:
            date =  datetime.datetime.strptime(date, '%m/%d/%Y').strftime('%Y-%m-%d')

        if address is not None:
            queryset = queryset.filter(club__address=address)

        if start_time and end_time:
            resource_id = Booking.objects.exclude(start_time__gte = start_time,
                                                  end_time__lte = end_time).values_list('resource_id')
            resource_id = [item[0] for item in resource_id]
            queryset = queryset.filter(id__in = resource_id)
        return queryset


class BookingFilter(BaseFilterBackend):
    """
    Returns queryset containing ...
    """
    # queryset = super(BookingViewSet, self).get_queryset()
    def filter_queryset(self, request, queryset, view):
        date = request.query_params.get('date', None)
        if date:
            date =  datetime.datetime.strptime(date, '%m/%d/%Y').strftime('%Y-%m-%d')

        if date is not None:
            queryset = Booking.objects.filter(date=date)

        return queryset
