from rest_framework import routers
from django.conf.urls import url, include, patterns

from facility.api import ClubViewSet, ResourceViewSet, BookingViewSet
from profiles.api import UserProfileViewSet, CurrentUserViewSet
from utils.api import SportsViewSet, AddressViewSet


router = routers.DefaultRouter()

router.register(r'user', UserProfileViewSet, base_name='user_profile')
router.register(r"me", CurrentUserViewSet, base_name="current_user")
router.register(r"club", ClubViewSet, base_name="club")
router.register(r"resource", ResourceViewSet, base_name="resource")
router.register(r"booking", BookingViewSet, base_name="booking")
router.register(r"sport", SportsViewSet, base_name="sport")
router.register(r"address", AddressViewSet, base_name="address")

urlpatterns = router.urls

urlpatterns = urlpatterns +  patterns("",
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include('allauth.urls')),
)
