from django.contrib.auth.models import User
from rest_framework import serializers

from profiles.models import UserProfile
from address.models import Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address


class UserProfileSerializer(serializers.ModelSerializer):
    """
        Serializer for user-profile
    """

    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.CharField(source='user.email')

    address = AddressSerializer()

    address_detail = serializers.SerializerMethodField('get_detail_address')

    def get_detail_address(self, obj):
        user_address = Address.objects.get(id=obj.id)
        dict = user_address.as_dict()
        return dict

    class Meta():
        model = UserProfile
        fields = (
            'id', 'first_name', 'last_name', 'email', 'contact_number',
            'about_me', 'address', 'address_detail')


    def _set_user_info(self, profile, user_data):
        user = profile.user
        for k, v in user_data.items():
            if hasattr(user, k):
                setattr(user, k, v)
        user.save()
        return user

    def save(self, **kwargs):
        user_data = None
        if self.validated_data.has_key("user"):
            user_data = self.validated_data.pop("user")

        profile = super(UserProfileSerializer, self).save(**kwargs)
        if user_data:
            self._set_user_info(profile, user_data)
        return profile

    def update(self, instance, validated_data):
        '''
        This function is overidden to allow nested writable serialization
        '''
        addrdict = validated_data.pop('address')

        #Save inner address object
        for attr, value in addrdict.items():
            setattr(instance.address, attr, value)
        instance.address.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        user = super(UserProfileSerializer, self).update(instance,validated_data)
        return user


class BaseUserSerializer(serializers.ModelSerializer):
    """
    Serializer for User Table
    """
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    is_authenticated = serializers.CharField(source='is_authenticated', read_only=True)

    class Meta:
        model = User


    def validate_email(self, attrs, source):
        """
        Check for unique email address
        """
        if attrs.has_key(source):
            queryset = self.Meta.model.objects.filter(email=attrs[source])
            if self.init_data.has_key("id"):
                if queryset.exclude(id=self.init_data["id"]).exists():
                    raise serializers.ValidationError("User with given email id already exists.")
            else:
                if queryset.exists():
                    raise serializers.ValidationError("User with given email id already exists.")
        return attrs


class CurrentUserSerializer(BaseUserSerializer):
    """
        for data to be sent for current logged in user
    """
    userprofile = UserProfileSerializer(read_only=True)

    class Meta(BaseUserSerializer.Meta):
        fields = ('id', 'first_name', 'last_name', 'full_name', 'email', 'userprofile')
        read_only_fields = ( 'email',)
