from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
import mock
import stripe


from utils.models import Address, Sports
from facility.models import Club, Resource, Booking
from profiles.models import UserProfile
from django.conf import settings

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
    address = Address.objects.create(lane1='13', lane2='b', area='andheri', city='mumbai',
                                     state='Maharashtra', country='India', latitude=12,
                                     longitude=23)

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
        'address': address,
        'sport': sport,
        'resource': resource,
        'booking': booking
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

    # def test_club_post(self):
    # # club = MODULE_DATA['club']
    # # user = MODULE_DATA['user']
    # address = MODULE_DATA['address']
    #
    #     data = {
    #     "name": "test club",
    #     "owner": user.id,
    #     "address": {
    #         "lane1": "222",
    #         "area": "karvenager",
    #         "city": "pune",
    #         "state": "Maharashtra",
    #         "country": "India"
    #     },
    #     "contact_number": "455454",
    #     "description": "sdfa"
    # }
    #     data = {"owner":user.id,
    #             "name":"new club",
    #             "description":"W",
    #             "contact_number":"12",
    #             "address":{"line1":"",
    #                        "line2":"",
    #                        "area":"EW",
    #                        "city":"WE",
    #                        "state":"WW",
    #                        "country":"WW",
    #                        "latitude":"31",
    #                        "longitude":"41",
    #                        "lane1":"1",
    #                        "lane2":"2"}}
    #     url = reverse('club-list')
    #     response = self.client.post(url, data)
    #     import ipdb; ipdb.set_trace()
    #     self.assertEqual(response.status_code, 200)


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
    def side_effect(self,amount=1, currency="usd", source="validToken", description="s"):
        self.assertEqual(source, "validToken")

    def setUp(self):
        credentials = {'username': MODULE_DATA['user'].email, "password": "test"}
        self.client.login(**credentials)

    def test_booking_get(self):
        url = reverse('booking-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_booking_post(self):
        stripe.Charge.create = mock.Mock(side_effect=self.side_effect)
        url = reverse('booking-list')
        user = MODULE_DATA['user']
        resource = MODULE_DATA['resource']

        data = {
        'user': user.id,
        'date': '2015-03-05',
        'start_time': '20:00:00',
        'end_time': '21:00:00',
        'resource': resource.id,
        'token': "validToken",
        'fee':1000
        }
        response = self.client.post(url, data)
        import ipdb;ipdb.set_trace()
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
