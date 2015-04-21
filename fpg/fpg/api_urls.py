from rest_framework import routers
from django.conf.urls import url, include
from facility.api import ClubView, ResourceView, BookingView
from profiles.api import UserProfileView, CurrentUserView
from utils.api import SportsView


router = routers.DefaultRouter()

router.register(r'user', UserProfileView, base_name='userprofile')
router.register(r"me", CurrentUserView, base_name="current_user")
router.register(r"club", ClubView, base_name="club")
router.register(r"resource", ResourceView, base_name="resource")
router.register(r"booking", BookingView, base_name="booking")
router.register(r"sports", SportsView, base_name="sports")


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]