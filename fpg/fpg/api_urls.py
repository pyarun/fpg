from rest_framework import routers
from django.conf.urls import url, include

from facility.api import ClubView, ResourceView, BookingView
from profiles.api import UserProfileViewSet, CurrentUserViewSet
from utils.api import SportsView


router = routers.DefaultRouter()

router.register(r'user', UserProfileViewSet, base_name='user_profile')
router.register(r"me", CurrentUserViewSet, base_name="current_user")
router.register(r"club", ClubView, base_name="club")
router.register(r"resource", ResourceView, base_name="resource")
router.register(r"booking", BookingView, base_name="booking")
router.register(r"sport", SportsView, base_name="sport")

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]