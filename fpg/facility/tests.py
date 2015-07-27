from datetime import datetime
from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
import mock
import stripe
import json

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


def create_resource(club, sport, name='test_club', open_time='06:00:00',
                    close_time='23:00:00', fee=1000,
                    status='available'):
    resource = Resource.objects.create(name=name, club=club, open_time=open_time,
                                       close_time=close_time, fee=fee, sport=sport,
                                       status=status)
    return resource


def create_booking(resource ,user, date, start_time, end_time):

    booking = Booking.objects.create(user=user, date=date, start_time=start_time,
                                     end_time=end_time, resource=resource)
    return booking


def setUpModule():
    """
        This function performs datatbase entry which we are using in test cases
    """
    super_user = create_superadmin()
    user_data = dict(username="test_user", email="test@gmail.com", password="test")
    address_data = dict(lane1='13', lane2='b', area='andheri', city='mumbai',
                        state='Maharashtra', country='India', latitude=12,
                        longitude=23)

    user = User.objects.create_user(**user_data)
    address = Address.objects.create(**address_data)

    userprofile_data = dict(user=user, contact_number='9899999', address=address,
                            about_me='good')

    UserProfile.objects.create(**userprofile_data)
    club_data = dict(name='test_club', owner=user, address=address,
                     contact_number='90887654')

    club = Club.objects.create(**club_data)
    sport = Sports.objects.create(name='khokho')

    resource = create_resource(club, sport)
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


class ClubAipTestCase(APITestCase):
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


class ResourceAipTestCase(APITestCase):
    """
        Test cases for resource end point.
    """

    def setUp(self):
        credentials = {'username': MODULE_DATA['user'].email, "password": "test"}
        self.client.login(**credentials)

    def test_list_resources(self):
        url = reverse('resource-list')
        response = self.client.get(url, format='json')
        sport = MODULE_DATA['sport']
        club = MODULE_DATA['club']
        resource = MODULE_DATA['resource']

        data = [{'status': resource.status, 'close_time': resource.close_time, 'fee': resource.fee,
                 'open_time': resource.open_time, 'club': club.id, 'photo': None,
                 'description': resource.description,
                 'name': 'test_club',
                 'sport_details': {'description': sport.description, 'name': sport.name,
                                   'id': sport.id},
                 'sport': sport.id, 'type': resource.type, 'id': resource.id,
                 'club_details': {'contact_number': club.contact_number,
                                  'description': club.description,
                                  'address': {'lane2': club.address.lane2,
                                              'lane1': club.address.lane1,
                                              'area': club.address.area,
                                              'country': club.address.country,
                                              'longitude': club.address.longitude,
                                              'state': club.address.state,
                                              'latitude': club.address.latitude,
                                              'id': club.address.id}, 'owner': '',
                                  'id': club.id,
                                  'name': club.name}}]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, data)

    def test_create_resource(self):
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
            'description': 'des'
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

        response_data = {'status': data['status'], 'close_time': data['close_time'],
                         'fee': data['fee'],
                         'open_time': data['open_time'], 'club': club.id, 'photo': None,
                         'description': data['description'],
                         'name': club.name,
                         'sport_details': {'description': None, 'id': sport.id, 'name': sport.name},
                         'sport': data['sport'], 'type': None, 'id': 2,
                         'club_details': {'contact_number': club.contact_number,
                                          'description': club.description,
                                          'address': {'state': club.address.state,
                                                      'lane2': club.address.lane2,
                                                      'lane1': club.address.lane1,
                                                      'area': club.address.area,
                                                      'latitude': club.address.latitude,
                                                      'country': club.address.country,
                                                      'id': club.address.id,
                                                      'longitude': club.address.longitude},
                                          'owner': '',
                                          'id': club.id, 'name': club.name}}

        self.assertEqual(response.data, response_data)

    def test_update_resource(self):
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
            'description': 'dsees'
        }

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 200)

        response_data = {'status': data['status'], 'close_time': data['close_time'],
                         'fee': data['fee'],
                         'open_time': data['open_time'], 'club': club.id, 'photo': None,
                         'description': data['description'],
                         'name': club.name,
                         'sport_details': {'description': None, 'id': sport.id, 'name': sport.name},
                         'sport': data['sport'], 'type': None,
                         'club_details': {'contact_number': club.contact_number,
                                          'description': club.description,
                                          'address': {'state': club.address.state,
                                                      'lane2': club.address.lane2,
                                                      'lane1': club.address.lane1,
                                                      'area': club.address.area,
                                                      'latitude': club.address.latitude,
                                                      'country': club.address.country,
                                                      'id': club.address.id,
                                                      'longitude': club.address.longitude},
                                          'owner': '',
                                          'id': club.id, 'name': club.name}}

        response.data.pop('id')
        self.assertEqual(response.data, response_data)

    def test_remove_resource(self):
        club = MODULE_DATA['club']
        sport = MODULE_DATA['sport']
        resource = create_resource(club=club, sport=sport)
        resource_id = resource.id
        url = reverse('resource-detail', args=(resource.id,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

        is_delete = Resource.objects.filter(id=resource_id).exists()
        self.assertEqual(is_delete, False)


class BookingApiTestCase(APITestCase):
    """
        Test cases for booking end point.
    """

    def side_effect(self, amount=1, currency="usd", source="validToken", description="s"):
        self.assertEqual(source, "validToken")

    def setUp(self):
        credentials = {'username': MODULE_DATA['user'].email, "password": "test"}
        self.client.login(**credentials)

    def test_list_bookings(self):
        url = reverse('booking-list')
        response = self.client.get(url)

        resource = MODULE_DATA['resource']
        booking = MODULE_DATA['booking']
        booking_date = datetime.strptime(booking.date, '%Y-%m-%d').strftime('%m/%d/%Y')
        self.assertEqual(response.status_code, 200)

        open_date_time = datetime.strptime('06:00:00', '%H:%M:%S')
        open_time = open_date_time.time()

        close_date_time = datetime.strptime('23:00:00', '%H:%M:%S')
        close_time = close_date_time.time()


        data = {'resource_details': {'status': resource.status, 'close_time': close_time,
                                     'fee': resource.fee, 'name': resource.name,
                                     'club': resource.club_id,
                                     'sport': resource.sport.name, 'type': resource.type,
                                     'open_time': open_time}, 'resource': resource.id,
                'title': booking.title, 'start_time': booking.start_time,
                'end_time': booking.end_time,
                'date': booking_date, 'id': booking.id, 'user': booking.user.id}


        self.test_data = response.data
        test_data = dict(self.test_data[0])
        self.assertEqual(test_data, data)


    def test_booking_post(self):
        stripe.Charge.create = mock.Mock(side_effect=self.side_effect)
        url = reverse('booking-list')
        user = MODULE_DATA['user']
        resource = MODULE_DATA['resource']
        open_date_time = datetime.strptime('06:00:00', '%H:%M:%S')
        open_time = open_date_time.time()

        close_date_time = datetime.strptime('23:00:00', '%H:%M:%S')
        close_time = close_date_time.time()


        data = {
            'user': user.id,
            'date': '03/05/2015',
            'start_time': '20:00:00',
            'end_time': '21:00:00',
            'resource': resource.id,
            'token': "validToken",
            'fee': 1000,
            'status': 'available'
        }


        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 201)


        response_data = {
        'resource_details': {'status': data['status'], 'close_time': close_time,
                             'fee': data['fee'], 'name': 'test_club', 'club': resource.club_id, 'sport': resource.sport.name,
                             'type': None, 'open_time': open_time}, 'resource': resource.id,
        'title': None, 'start_time': data['start_time'], 'end_time': data['end_time'], 'date': data['date'],
        'user': user.id}

        response.data.pop('id')
        self.assertEqual(response.data, response_data)
        

    def test_booking_put(self):
        booking = MODULE_DATA['booking']
        url = reverse('booking-detail', args=(booking.id,))
        user = MODULE_DATA['user']
        resource = MODULE_DATA['resource']

        data = {
            'user': user.id,
            'date': '03/05/2015',
            'start_time': '20:00:00',
            'end_time': '21:00:00',
            'resource': resource.id,
            'fee': 1000,
            'status': 'available'
        }

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 200)

        open_date_time = datetime.strptime('06:00:00', '%H:%M:%S')
        open_time = open_date_time.time()

        close_date_time = datetime.strptime('23:00:00', '%H:%M:%S')
        close_time = close_date_time.time()

        response_data = {
        'resource_details': {'status': data['status'], 'close_time': close_time,
                             'fee': data['fee'], 'name': 'test_club', 'club': resource.club_id, 'sport': resource.sport.name,
                             'type': None, 'open_time': open_time}, 'resource': resource.id,
        'title': None, 'start_time': data['start_time'], 'end_time': data['end_time'], 'date': data['date'],
        'id':booking.id, 'user': user.id}

        self.assertEqual(response.data, response_data)


    def test_booking_delete(self):
        resource = MODULE_DATA['resource']
        user = MODULE_DATA['user']

        booking = create_booking(resource, user, start_time="12:00:00", end_time="13:00:00", date='2015-03-03')

        url = reverse('booking-detail', args=(booking.id,))
        booking_id = booking.id
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        is_delete = Booking.objects.filter(id=booking_id).exists()
        self.assertEqual(is_delete, False)
