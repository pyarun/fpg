from rest_framework import viewsets
from utils.models import Sports
from utils.serializers import SportSerializer


class SportsView(viewsets.ModelViewSet):
    """
        create, delete, update, list sports
    """
    model = Sports
    serializer_class = SportSerializer
    queryset = Sports.objects.all()