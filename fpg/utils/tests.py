import json

from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


# Create your tests here.
from utils.models import Sports


def create_sport(name):
    sport = Sports.objects.create(name=name)

    return sport


def create_superadmin(username="admin", email="admin@admin.com", password="admin"):
    """
        This function creates super admin
    """
    user = User.objects.create_superuser(username=username, email=email, password=password)
    return user


MODULE_test_data = {}


def setUpModule():
    """
        This function performs test_datatbase entry which we are using in test cases
    """
    super_user = create_superadmin()
    user = User.objects.create_user("test_user", email="test@gmail.com", password="password")

    sport = create_sport(name="khokho")

    MODULE_test_data.update({
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

    def test_sport_list(self):
        url = reverse('sport-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        sport_dict = response.data
        sport_dict = json.dumps(sport_dict)
        sport_dict = json.loads(sport_dict)

        for sdict in sport_dict:
            self.assertEqual(sdict['name'], Sports.objects.get(id=sdict['id']).name)


    def test_sport_create(self):
        url = reverse('sport-list')
        test_data = {
            'name': 'Rugby',
            'description': 'faffa'
        }

        response = self.client.post(url, test_data)
        self.assertEqual(response.status_code, 201)
        response.data.pop('id')
        self.assertEqual(response.data,
                         {'description': test_data['description'], 'name': test_data['name']})

    def test_sport_update(self):
        sport = MODULE_test_data['sport']
        url = reverse('sport-detail', args=(sport.id,))
        test_data = {
            'name': 'Rugby',
            'description': 'faffa'
        }

        response = self.client.put(url, test_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data,
                         {'id': sport.id, 'name': test_data['name'],
                          'description': test_data['description']})

    def test_sport_delete(self):
        sport = create_sport(name="fifa")
        sport_id = sport.id
        url = reverse('sport-detail', args=(sport.id,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        is_deleted = Sports.objects.filter(id=sport_id).exists()
        self.assertEqual(is_deleted, False)
