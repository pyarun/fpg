from rest_framework import viewsets
from utils.models import Sports, Address
from utils.serializers import SportSerializer, AddressSerializer


class SportsView(viewsets.ModelViewSet):
    """
        create, delete, update, list sports
    """
    model = Sports
    serializer_class = SportSerializer
    queryset = Sports.objects.all()


class AddressView(viewsets.ModelViewSet):
    """
        create, delete, update, list address
    """
    model = Address
    serializer_class = AddressSerializer
    queryset = Address.objects.all()