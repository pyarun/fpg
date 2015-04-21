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
        fields = ('id', 'name', 'owner', 'address', 'contact_number', 'description')


class ResourceSerializer(serializers.ModelSerializer):
    """
        For create, update, delete, list resources.
    """
    club = serializers.SerializerMethodField('club_info')
    sport = serializers.SerializerMethodField('sport_info')

    class Meta:
        model = Resource
        fields = ('id', 'name', 'type', 'club', 'open_time', 'close_time', 'fee', 'sport', 'photo',
                  'status', 'description')

    def club_info(self, obj):
        club = obj.club

        club_dict = {'id': club.id,
                     'name': club.name,
                     'owner': club.owner.get_full_name(),
                     'contact_number': club.contact_number,
                     'description': club.description,
                     'address': {
                         'id': club.address.id,
                         'country': club.address.locality.state.country.name,
                         'state': club.address.locality.state.name,
                         'raw': club.address.raw,
                         'route': club.address.route,
                         'locality': club.address.locality.name,
                         'postal_code': club.address.locality.postal_code,
                         'latitude': club.address.latitude,
                         'longitude': club.address.longitude,

                     }
        }

        return club_dict


    def sport_info(selfn, obj):
        sport = Sports.objects.get(id=obj.id)
        sport_dict = {
            'id': sport.id,
            'name': sport.name,
            'description': sport.description
        }

        return sport_dict


class BookingSerializer(serializers.ModelSerializer):
    '''
        For create, update, list, delete bookings
    '''

    resource = serializers.SerializerMethodField('resource_info')

    class Meta:
        model = Booking
        fields = ('id', 'user', 'title', 'date', 'start_time', 'end_time', 'resource')

    def resource_info(self, obj):
        resource = obj.resource

        # import ipdb; ipdb.set_trace()
        resource_dict = {
            'name': resource.name,
            'type': resource.type,
            'open_time': resource.open_time,
            'close_time': resource.close_time,
            'status': resource.status,
            'sport': resource.sport.name,
            'photo': resource.photo.url,
            'fee': resource.fee,
            'club': resource.club.id
        }
        return resource_dict


