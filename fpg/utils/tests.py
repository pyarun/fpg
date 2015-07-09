from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

# Create your tests here.
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

    sport = Sports.objects.create(name='khokho')

    MODULE_DATA.update({
        'super_user': super_user,
        'user': user,
        'sport': sport,
    })


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
            'detail': 'faffa'
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    def test_sport_put(self):
        sport = MODULE_DATA['sport']
        url = reverse('sport-detail', args=(sport.id,))
        data = {
            'name': 'Rugby',
            'detail': 'faffa'
        }

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 200)

    def test_sport_patch(self):
        sport = MODULE_DATA['sport']
        url = reverse('sport-detail', args=(sport.id,))
        data = {
            'name': 'Rugby',
            'detail': 'faffa'
        }

        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)

    def test_sport_delete(self):
        sport = MODULE_DATA['sport']
        url = reverse('sport-detail', args=(sport.id,))

        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
