import stripe
import logging

from rest_framework import viewsets
from facility.filters import BookingFilter, ResourceFilter

from facility.models import Club, Resource, Booking
from facility.serializers import ClubSerializer, ResourceSerializer, BookingSerializer
from fpg.settings import STRIPE_API_KEY

logger = logging.getLogger("fpg")

class ClubViewSet(viewsets.ModelViewSet):
    """
        Create update delete and list the clubs
    """
    model = Club
    serializer_class = ClubSerializer
    queryset = Club.objects.all()
    filter_fields = ('id' ,'owner', 'address')
    filter_backends = viewsets.ModelViewSet.filter_backends


class ResourceViewSet(viewsets.ModelViewSet):
    """
        To list, create, update, delete resources.
    """
    model = Resource
    serializer_class = ResourceSerializer
    queryset = Resource.objects.all()
    filter_fields = ('id' ,'club', 'sport')
    filter_backends = viewsets.ModelViewSet.filter_backends + [ResourceFilter]


class BookingViewSet(viewsets.ModelViewSet):
    """
        To list, create, update, delete bookings
    """
    model = Booking
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()
    filter_fields = ('id','resource',)
    filter_backends = viewsets.ModelViewSet.filter_backends + [BookingFilter]

    def create(self, request, *args, **kwargs):
        """
            we have over-ride this function
            This function will create booking entry in database after successful payment
        """
        # This is a secrete key of user's account to whom the payment will arrive.
        stripe.api_key = STRIPE_API_KEY

        # This is token generated by stripe
        token = request.DATA['token']


        # Create the charge on Stripe's servers - this will charge the user's card
        try:
            charge = stripe.Charge.create(
              amount=request.DATA['fee'], # amount in cents, again
              currency="usd",
              source=token,
              description="Example charge"
            )

        except stripe.error.CardError, e:
            # The card has been declined
            logger.debug(e)

        return super(BookingViewSet, self).create(request, *args, **kwargs)
