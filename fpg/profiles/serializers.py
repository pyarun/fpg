from django.contrib.auth.models import User
from rest_framework import serializers

from profiles.models import UserProfile
from utils.models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address


class UserProfileSerializer(serializers.ModelSerializer):
    """
        Serializer for user-profile
    """
    address = AddressSerializer(required=False)

    class Meta():
        model = UserProfile
        fields = (
            'id', 'contact_number', 'about_me', 'address', )

    def _set_user_info(self, profile, user_data):
        user = profile.user
        for k, v in user_data.items():
            if hasattr(user, k):
                setattr(user, k, v)
        user.save()
        return user

    def save(self, **kwargs):
        """
        Overridden to allow saving additional information, which donot directly maps to
        Profile Model
        """
        user_data = None
        if self.validated_data.has_key("user"):
            user_data = self.validated_data.pop("user")

        profile = super(UserProfileSerializer, self).save(**kwargs)
        if user_data:
            self._set_user_info(profile, user_data)
        return profile

    def update(self, instance, validated_data):
        '''
        Overridden to allow nested writable serialization
        '''
        addrdict = None
        if validated_data.has_key("address"):
            addrdict = validated_data.pop('address')

        profile = super(UserProfileSerializer, self).update(instance, validated_data)

        if addrdict:
            add_serializer = AddressSerializer(profile.address, addrdict, partial=True)
            if add_serializer.is_valid():
                add_serializer.save()

        return profile


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
    profile = UserProfileSerializer()

    class Meta(BaseUserSerializer.Meta):
        fields = ('id', 'first_name', 'last_name', 'full_name', 'email', 'profile')
        read_only_fields = ( 'email',)


    def update(self, instance, validated_data):
        """
        This function is overidden to allow nested writable serialization
        """
        profiledict = validated_data.pop('profile')
        address = profiledict.pop('address')

        # Save address
        for attr, value in address.iteritems():
            setattr(instance.profile.address, attr, value)
        instance.profile.address.save()

        # save userprofile
        for attr, value in profiledict.iteritems():
            if attr == 'user':
                value = instance
            setattr(instance.profile, attr, value)
        instance.profile.save()

        # save rest fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        user = super(CurrentUserSerializer, self).update(instance, validated_data)
        return user
