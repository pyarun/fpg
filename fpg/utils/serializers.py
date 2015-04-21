from rest_framework import serializers
from utils.models import Sports

class SportSerializer(serializers.ModelSerializer):
    '''
        For create, update, delete, list operations
    '''
    class Meta:
        model = Sports
        fields = ('id', 'name', 'description')