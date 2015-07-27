from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from profiles.models import UserProfile
from utils.models import Address


def create_superadmin(username="admin", email="admin@admin.com", password="admin"):
    """
        This function creates super admin
    """
    user = User.objects.create_superuser(username=username, email=email, password=password)
    return user


def setUpModule():
    """
        This function performs datatbase entry which we are using in test cases
    """
    create_superadmin()
    user = User.objects.create_user("test_user", email="test@gmail.com", password="password")

    address = Address.objects.create(lane1='lane1', area='karvenager', city='pune',
                                     state='maharashtra', country='india')

    UserProfile.objects.create(user=user, contact_number='9899999', address=address,
                               about_me='good')


class TestApiUser(APITestCase):
    """
        Test case for user end point
    """

    def setUp(self):
        credentials = {'username': 'admin@admin.com', "password": "admin"}
        self.client.login(**credentials)

    def test_user_get(self):
        user = UserProfile.objects.all()[0]
        user_id = user.id
        url = reverse('user_profile-detail', args=(user_id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        data = {'contact_number': user.contact_number, 'about_me': user.about_me, 'id': user_id,
                'address': {'city': user.address.city, 'lane2': user.address.lane2,
                            'lane1': user.address.lane1,
                            'area': user.address.area, 'country': user.address.country,
                            'longitude': user.address.longitude,
                            'state': user.address.state, 'latitude': user.address.latitude,
                            'id': user.address.id}}

        self.assertEqual(response.data, data)

    def test_user_put(self):
        user = UserProfile.objects.all()[0]
        user_id = user.id
        data = {
            'contact_number': '9899898',
            'about_me': 'cool'
        }

        url = reverse('user_profile-detail', args=(user_id,))
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, 200)

        data = {'contact_number': data['contact_number'], 'about_me': data['about_me'],
                'id': user_id,
                'address': {'city': user.address.city, 'lane2': user.address.lane2,
                            'lane1': user.address.lane1,
                            'area': user.address.area, 'country': user.address.country,
                            'longitude': user.address.longitude,
                            'state': user.address.state, 'latitude': user.address.latitude,
                            'id': user.address.id}}

        self.assertEqual(response.data, data)

