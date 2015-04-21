from address.models import Address
from rest_framework import serializers

from facility.models import Club, Resource, Booking
from profiles.serializers import AddressSerializer


class ClubSerializer(serializers.ModelSerializer):
    """
        User can create, update, list and delete Clubs
    """
    address = AddressSerializer()

    class Meta:
        model = Club
        fields = ('id', 'name', 'owner', 'address', 'contact_number', 'description')

    def create(self, validated_data):
        """
        This function is overidden to allow nested writable serialization
        """
        addrdict = validated_data.pop('address')
        addrobj = Address.objects.create(**addrdict)
        validated_data['address'] = addrobj
        club = super(ClubSerializer, self).create(validated_data)
        return club


    def update(self, instance, validated_data):
        '''
        Overridden to allow nested writable serialization
        '''
        addrdict = validated_data.pop('address')

        # Save inner address object
        for attr, value in addrdict.items():
            setattr(instance.address, attr, value)
        instance.address.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        club = super(ClubSerializer, self).update(instance, validated_data)
        return club


class ResourceSerializer(serializers.ModelSerializer):
    """
        For create, update, delete, list resources.
    """
    club_details = serializers.SerializerMethodField('club_info')
    sport_details = serializers.SerializerMethodField('sport_info')
    class Meta:
        model = Resource
        fields = ('id', 'name', 'type', 'club', 'club_details', 'open_time', 'close_time', 'fee', 'sport', 'sport_details', 'photo',
                  'status', 'description')

    def club_info(self, obj):
        club_object = obj.club

        club_dict = {   'id': club_object.id,
                        'name': club_object.name,
                        'owner': club_object.owner.get_full_name(),
                        'contact_number':club_object.contact_number,
                        'description':club_object.description,
                        'address': {
                            'id': club_object.address.id,
                            'country': club_object.address.locality.state.country.name,
                            'state':club_object.address.locality.state.name,
                            'raw': club_object.address.raw,
                            'route': club_object.address.route,
                            'locality':club_object.address.locality.name,
                            'postal_code': club_object.address.locality.postal_code,
                            'latitude': club_object.address.latitude,
                            'longitude': club_object.address.longitude,

                        }
        }
        return club_dict


    def sport_info(selfn, obj):
        sport_object = obj.sport
        sport_dict = {
                        'id': sport_object.id,
                        'name':sport_object.name,
                        'description': sport_object.description
        }
        return sport_dict



class BookingSerializer(serializers.ModelSerializer):
    """
        For create, update, list, delete bookings
    """
    resource_details = serializers.SerializerMethodField('resource_info')

    class Meta:
        model = Booking
        fields = ('id', 'user', 'title', 'date', 'start_time', 'end_time', 'resource', 'resource_details' )


    def resource_info(self, obj):
        resource = obj.resource

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

