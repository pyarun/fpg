from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated

from profiles.models import UserProfile
from profiles.serializers import UserProfileSerializer, CurrentUserSerializer


class UserProfileOwnerOrReadOnly(permissions.BasePermission):
    """
        Allows update, delete operations to owner of the profile.
        Restrict other users to Read only access.
        Superusers can preform all operations on user profiles
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user


class UserProfileViewSet(viewsets.mixins.RetrieveModelMixin,
                         viewsets.mixins.UpdateModelMixin,
                         viewsets.mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    """
        User profile view to list, update, retrive the user profiles
    """
    serializer_class = UserProfileSerializer
    model = UserProfile
    queryset = UserProfile.objects.all()

    permission_classes = (
        UserProfileOwnerOrReadOnly,
    )


class CurrentUserViewSet(viewsets.mixins.RetrieveModelMixin,
                         viewsets.mixins.UpdateModelMixin,
                         viewsets.mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    model = User
    # serializer_class = UserProfileSerializer
    serializer_class = CurrentUserSerializer
    permission_classes = [IsAuthenticated]



    def get_object(self, queryset=None):
       return self.request.user

    def list(self, request, *args, **kwargs):
        return self.retrieve(request)

    def update(self, request, *args, **kwargs):
        # import ipdb;ipdb.set_trace()
        kwargs["partial"] = True
        return super(CurrentUserViewSet, self).update(request, *args, **kwargs)



    # def pre_save(self, obj):
    #     if self.request.DATA.has_key("password") and self.request.DATA["password"]:
    #         obj.set_password(self.request.DATA["password"])

        # CurrentUserViewSet.pre_save(self, obj)

    #add a additional view to allow password reset
    # def reset_password(self):

# class CountryViewSet(viewsets.mixins.RetrieveModelMixin,
#                          viewsets.mixins.UpdateModelMixin,
#                          viewsets.mixins.ListModelMixin,
#                          viewsets.GenericViewSet):
#     """
#
#     """
#     serializer_class = CountrySerializer
#     model = Country
#     queryset = Country.objects.all()
