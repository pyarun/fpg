from django.test import TestCase

# Create your tests here.

from address.models import Address, Country, State, Locality
from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

# Create your tests here.
from facility.models import Club
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
    user = User.objects.create_user("test_user", email="test@gmail.com", password="password")

    # user = User.objects.create(username='abc',first_name='f',last_name='l',email='abc@abc.com', password='abc')
    # address = Address.objects.create(lane1='lane1', area='karvenager', city='pune',
    #                                  state='maharashtra', country='india')

    country = Country.objects.create(name = 'India', code='IN')
    state = State.objects.create(name= 'Maharashtra', code='MH', country=country)
    locality = Locality.objects.create(name='karvenagar', postal_code='411052', state=state)
    address = Address.objects.create(raw = '1234', locality = locality)

    UserProfile.objects.create(user=user, contact_number='9899999', address=address,
                               about_me='good')

    club = Club.objects.create(name='test_club', owner=user, address=address, contact_number='90887654')
    sport = Sports.objects.create(name='khokho')

    MODULE_DATA.update({
        'super_user':super_user,
        'user':user,
        'club':club,
        'locality': locality,
        'sport':sport
    })


class TestApiClub(APITestCase):
    """
        Test case for club end point
    """

    def setUp(self):
        credentials = {'username': 'admin@admin.com', "password": "admin"}
        self.client.login(**credentials)


    def test_club_get(self):
        url = reverse('club-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_club_post(self):
        club = MODULE_DATA['club']
        user = MODULE_DATA['user']
        address = club.address
        locality = MODULE_DATA['locality']

        data = {
            'name': 'test_club',
            'owner': user.id,
            'contact_number': '987696',
            'formatted':'sangvi',
            'locality': locality,
            'contact_number': '9887678',
            'latitude':12,
            'longitude':34,
            'raw': '06788'
        }

        url = reverse('club-list')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    # def test_club_patch(self):
    #     club_id = Club.objects.all()[0].id
    #     user = User.objects.all()[0]
    #     address = Address.objects.all()[0]
    #
    #     data = {
    #         'name': 'test_club',
    #         'owner': user,
    #         'address': address,
    #         'contact_number': '987696',
    #     }
    #     url = reverse('club-detail',args=(club_id,))
    #     response = self.client.patch(url,data)
    #
    #     self.assertEqual(response.status_code, 200)


class TestApiSport(APITestCase):
    """
        Test cases for sport end point
    """
    def setUp(self):
        credentials = {'username': 'admin@admin.com', "password": "admin"}
        self.client.login(**credentials)

    def test_sport_get(self):
        url = reverse('sport-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_sport_post(self):
        url = reverse('sport-list')
        data = {
            'name': 'Rugby',
            'detail':'faffa'
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    def test_sport_put(self):
        sport = MODULE_DATA['sport']
        url = reverse('sport-detail',args=(sport.id,))
        data = {
            'name': 'Rugby',
            'detail':'faffa'
        }

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 200)

    def test_sport_patch(self):
        sport = MODULE_DATA['sport']
        url = reverse('sport-detail',args=(sport.id,))
        data = {
            'name': 'Rugby',
            'detail':'faffa'
        }

        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)

    def test_sport_delete(self):
        sport = MODULE_DATA['sport']
        url = reverse('sport-detail',args=(sport.id,))

        response = self.client.delete(url)
        import ipdb;ipdb.set_trace()
        self.assertEqual(response.status_code, 204)