from rest_framework import serializers

from utils.models import Sports, Address


class SportSerializer(serializers.ModelSerializer):
    """
        For create, update, delete, list operations
    """
    class Meta:
        model = Sports
        fields = ('id', 'name', 'description')


class AddressSerializer(serializers.ModelSerializer):
    """
        For create, update, delete, list operations
    """
    class Meta:
        model = Address
        fields = ('id', 'city', 'area')