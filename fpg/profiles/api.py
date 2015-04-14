from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.viewsets import GenericViewSet

from profiles.models import UserProfile
from profiles.serializers import UserProfileSerializer, CurrentUserSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
         Logged in user can edit their own profile, but cannot edit other's profile.
         They can see others profile. Superuser can access all profiles
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user


class UserProfileView(viewsets.mixins.RetrieveModelMixin,
                      viewsets.mixins.UpdateModelMixin,
                      # viewsets.mixins.ListModelMixin,
                      viewsets.GenericViewSet,
):
    '''
        User profile view to list, update, retrive the user profiles
    '''

    serializer_class = UserProfileSerializer
    model = UserProfile
    queryset = UserProfile.objects.all()

    permission_classes = (
        IsOwnerOrReadOnly,
    )


class CurrentUserView(viewsets.mixins.RetrieveModelMixin,
                      viewsets.mixins.UpdateModelMixin,
                      viewsets.mixins.ListModelMixin, GenericViewSet):
    model = User
    serializer_class = CurrentUserSerializer

    def get_object(self, queryset=None):
        return self.request.user

    def list(self, request, *args, **kwargs):
        return self.retrieve(request)

    def pre_save(self, obj):
        if self.request.DATA.has_key("password") and self.request.DATA["password"]:
            obj.set_password(self.request.DATA["password"])

        GenericViewSet.pre_save(self, obj)
