from rest_framework import serializers

from facility.models import Club, Resource, Booking
from profiles.serializers import AddressSerializer
from utils.models import Sports, Address


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
        import ipdb;ipdb.set_trace()
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


    def create(self, validated_data):
        """
        This function is overridden to allow nested writable serialization
        """
        address = validated_data.pop('address')
        address_obj = Address.objects.create(**address)
        validated_data['address'] = address_obj
        club = super(ClubSerializer, self).create(validated_data)
        return club

    def update(self, instance, validated_data):
        """
        This function is overridden to allow nested writable serialization
        """
        address = validated_data.pop('address')

        # Save address
        for attr, value in address.iteritems():
            setattr(instance.address, attr, value)
        instance.address.save()

        # save rest fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        user = super(ClubSerializer, self).update(instance, validated_data)
        return user


class ResourceSerializer(serializers.ModelSerializer):
    """
        For create, update, delete, list resources.
    """
    club_details = serializers.SerializerMethodField('club_info')
    sport_details = serializers.SerializerMethodField('sport_info')
    class Meta:
        model = Resource
        fields = ('id', 'name', 'type', 'club', 'club_details', 'open_time', 'close_time',
                  'fee', 'sport', 'sport_details', 'photo', 'status', 'description')

    def club_info(self, obj):
        club = obj.club

        club_dict = {'id': club.id,
                     'name': club.name,
                     'owner': club.owner.get_full_name(),
                     'contact_number': club.contact_number,
                     'description': club.description,
                     'address': {
                         'id': club.address.id,
                         'country': club.address.country,
                         'state': club.address.state,
                         'lane1':club.address.lane1,
                         'lane2':club.address.lane2,
                         'area':club.address.area,
                         'latitude': club.address.latitude,
                         'longitude': club.address.longitude,
                     }
        }
        return club_dict


    def sport_info(selfn, obj):
        sport = obj.sport
        sport_dict = {
                        'id': sport.id,
                        'name':sport.name,
                        'description': sport.description
        }
        return sport_dict



class BookingSerializer(serializers.ModelSerializer):
    """
        For create, update, list, delete bookings
    """
    resource_details = serializers.SerializerMethodField('resource_info')

    class Meta:
        model = Booking
        fields = ('id', 'user', 'title', 'date', 'start_time', 'end_time', 'resource',
                  'resource_details' )


    def resource_info(self, obj):
        resource = obj.resource

        resource_dict = {
            'name': resource.name,
            'type': resource.type,
            'open_time': resource.open_time,
            'close_time': resource.close_time,
            'status': resource.status,
            'sport': resource.sport.name,
            'fee': resource.fee,
            'club': resource.club.id
        }
        return resource_dict
