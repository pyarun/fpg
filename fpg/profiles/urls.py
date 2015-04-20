from rest_framework import routers
from django.conf.urls import patterns, include, url

from profiles.api import UserProfileView, CurrentUserView, ClubView, ResourceView


router = routers.DefaultRouter()
router.register(r'user', UserProfileView, base_name='userprofile')
router.register(r"me", CurrentUserView, base_name="current_user")
router.register(r"club", ClubView, base_name="club")
router.register(r"resource", ResourceView, base_name="resource")

urlpatterns = patterns('',
                       url(r'^api-auth/',
                           include('rest_framework.urls', namespace='rest_framework')),
                       url(r"^", include(router.urls)),
)
