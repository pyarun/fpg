from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from address.models import Address, Country, State, Locality

from facility.models import Club, Resource, Booking
from profiles.models import UserProfile
from utils.models import Sports


def create_superadmin(username="admin", email="admin@admin.com", password="admin"):
    """
        This function creates super admin
    """
    user = User.objects.create_superuser(username=username, email=email, password=password)
    return user


MODULE_DATA = {}


def setUpModule():
    """
        This function performs datatbase entry which we are using in test cases
    """
    super_user = create_superadmin()
    user = User.objects.create_user("test_user", email="test@gmail.com", password="test")
    country = Country.objects.create(name='India', code='IN')
    state = State.objects.create(name='Maharashtra', code='MH', country=country)
    locality = Locality.objects.create(name='karvenagar', postal_code='411052', state=state)
    address = Address.objects.create(raw='1234', locality=locality)
    UserProfile.objects.create(user=user, contact_number='9899999', address=address,
                               about_me='good')

    club = Club.objects.create(name='test_club', owner=user, address=address,
                               contact_number='90887654')
    sport = Sports.objects.create(name='khokho')
    resource = Resource.objects.create(name='test_club', club=club, open_time='06:00:00',
                                       close_time='23:00:00', fee=1000, sport=sport,
                                       status='available')

    booking = Booking.objects.create(user=user, date="2015-04-25", start_time="20:00:09",
                                     end_time="21:00:00", resource=resource)

    MODULE_DATA.update({
        'super_user': super_user,
        'user': user,
        'club': club,
        'locality': locality,
        'sport': sport,
        'resource': resource,
        'booking': booking,
        'address': address
    })


class TestApiClub(APITestCase):
    """
        Test case for club end point
    """
    def setUp(self):
        credentials = {'username': MODULE_DATA['user'].email, "password": "test"}
        self.client.login(**credentials)


    def test_club_get(self):
        url = reverse('club-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_club_post(self):
        club = MODULE_DATA['club']
        user = MODULE_DATA['user']
        address = MODULE_DATA['address']

        locality = MODULE_DATA['locality']

        data = {
        "name": "test club",
        "owner": user.id,
        "address": {
            "street_number": "222",
            "route": "22",
            "raw": "2",
            "formatted": "karvenager",
            "latitude": -3.0,
            "longitude": 5.0,
            "locality": locality
        },
        "contact_number": "455454",
        "description": "sdfa"
    }

        url = reverse('club-list')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)


class TestAipResource(APITestCase):
    """
        Test cases for resource end point.
    """
    def setUp(self):
        credentials = {'username': MODULE_DATA['user'].email, "password": "test"}
        self.client.login(**credentials)

    def test_resource_get(self):
        url = reverse('resource-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_resource_post(self):
        url = reverse('resource-list')
        club = MODULE_DATA['club']
        sport = MODULE_DATA['sport']

        data = {
            'name': 'test_club',
            'club': club.id,
            'open_time': '06:00:00',
            'close_time': '23:00:00',
            'fee': 1000,
            'sport': sport.id,
            'status': 'available',
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    def test_resource_put(self):
        resource = MODULE_DATA['resource']
        club = MODULE_DATA['club']
        sport = MODULE_DATA['sport']

        url = reverse('resource-detail', args=(resource.id,))

        data = {
            'name': 'test_club',
            'club': club.id,
            'open_time': '06:00:00',
            'close_time': '23:00:00',
            'fee': 1000,
            'sport': sport.id,
            'status': 'available',
        }

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 200)


    def test_resource_patch(self):
        resource = MODULE_DATA['resource']
        club = MODULE_DATA['club']
        sport = MODULE_DATA['sport']

        url = reverse('resource-detail', args=(resource.id,))

        data = {
            'name': 'test_club',
            'club': club.id,
            'open_time': '06:00:00',
            'close_time': '23:00:00',
            'fee': 1000,
            'sport': sport.id,
            'status': 'available',
        }

        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)

    def test_resource_delete(self):
        resource = MODULE_DATA['resource']
        url = reverse('resource-detail', args=(resource.id,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)


class TestApiBooking(APITestCase):
    """
        Test cases for booking end point.
    """
    def setUp(self):
        credentials = {'username': MODULE_DATA['user'].email, "password": "test"}
        self.client.login(**credentials)

    def test_booking_get(self):
        url = reverse('booking-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_booking_post(self):
        url = reverse('booking-list')
        user = MODULE_DATA['user']
        resource = MODULE_DATA['resource']

        data = {
            'user': user.id,
            'date': '2015-03-05',
            'start_time': '20:00:00',
            'end_time': '21:00:00',
            'resource': resource.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    def test_booking_put(self):
        booking = MODULE_DATA['booking']
        url = reverse('booking-detail', args=(booking.id,))
        user = MODULE_DATA['user']
        resource = MODULE_DATA['resource']

        data = {
            'user': user.id,
            'date': '2015-03-05',
            'start_time': '20:00:00',
            'end_time': '21:00:00',
            'resource': resource.id,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 200)

    def test_booking_patch(self):
        booking = MODULE_DATA['booking']
        url = reverse('booking-detail', args=(booking.id,))
        user = MODULE_DATA['user']
        resource = MODULE_DATA['resource']

        data = {
            'user': user.id,
            'date': '2015-03-05',
            'start_time': '20:00:00',
            'end_time': '21:00:00',
            'resource': resource.id,
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)

    def test_booking_delete(self):
        booking = MODULE_DATA['booking']
        url = reverse('booking-detail', args=(booking.id,))

        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)


