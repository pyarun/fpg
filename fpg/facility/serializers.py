from rest_framework import serializers
from facility.models import Club, Resource, Booking

from profiles.serializers import AddressSerializer
from utils.models import Sports


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

    club = serializers.SerializerMethodField('club_info')
    sport = serializers.SerializerMethodField('sport_info')

    def club_info(self, obj):
        object = obj.club

        club_dict = {   'id': object.id,
                        'name': object.name,
                        'owner': object.owner.get_full_name(),
                        'contact_number':object.contact_number,
                        'description':object.description,
                        'address': {
                            'id': object.address.id,
                            'country': object.address.locality.state.country.name,
                            'state':object.address.locality.state.name,
                            'raw': object.address.raw,
                            'route': object.address.route,
                            'locality':object.address.locality.name,
                            'postal_code': object.address.locality.postal_code,
                            'latitude': object.address.latitude,
                            'longitude': object.address.longitude,

                        }
        }

        return club_dict


    def sport_info(selfn, obj):

        object = Sports.objects.get(id=obj.id)
        sport_dict = {
                        'id': object.id,
                        'name':object.name,
                        'description': object.description
        }

        return sport_dict

    class Meta:
        model = Resource
        fields = ('id', 'name', 'type', 'club', 'open_time', 'close_time', 'fee', 'sport', 'photo',
                  'status', 'description')


class BookingSerializer(serializers.ModelSerializer):
    '''
        For create, update, list, delete bookings
    '''

    resource = serializers.SerializerMethodField('resource_info')

    def resource_info(self, obj):
        resouce_object = obj.resource

        # import ipdb; ipdb.set_trace()
        resource_dict = {
                        'name' : resouce_object.name,
                        'type': resouce_object.type,
                        'open_time': resouce_object.open_time,
                        'close_time': resouce_object.close_time,
                        'status' : resouce_object.status,
                        'sport' : resouce_object.sport.name,
                        'photo' : resouce_object.photo.url,
                        'fee' : resouce_object.fee,
                        'club' : resouce_object.club.id
        }
        return resource_dict

    class Meta:
        model = Booking
        fields = ('id', 'user', 'title', 'date', 'start_time', 'end_time', 'resource')
