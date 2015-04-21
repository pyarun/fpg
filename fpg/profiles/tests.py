from address.models import Address, Country, State, Locality
from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

# Create your tests here.
from profiles.models import UserProfile


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

    # user = User.objects.create(username='abc',first_name='f',last_name='l',email='abc@abc.com', password='abc')
    # address = Address.objects.create(lane1='lane1', area='karvenager', city='pune',
    #                                  state='maharashtra', country='india')

    country = Country.objects.create(name = 'India', code='IN')
    state = State.objects.create(name= 'Maharashtra', code='MH', country=country)
    locality = Locality.objects.create(name='karvenagar', postal_code='411052', state=state)
    address = Address.objects.create(raw = '1234', locality = locality)

    UserProfile.objects.create(user=user, contact_number='9899999', address=address,
                               about_me='good')


class TestApiUser(APITestCase):
    """
        Test case for user end point
    """

    def setUp(self):
        # self.user = create_superadmin()
        credentials = {'username': 'admin@admin.com', "password": "admin"}
        self.client.login(**credentials)

    def test_user_get(self):
        user_id = UserProfile.objects.all()[0].id
        url = reverse('user_profile-detail', args=(user_id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_user_put(self):
        user_id = UserProfile.objects.all()[0].id
        data = {
            'contact_number': '9899898',
            'area': 'kothrud',
            'about_me': 'cool'
        }

        url = reverse('user_profile-detail', args=(user_id,))
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
