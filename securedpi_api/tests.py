from django.test import TestCase
from django.contrib.auth.models import User
from securedpi_locks.models import Lock
from securedpi_events.models import Event
from rest_framework import status
from rest_framework.test import APITestCase


class APIAccessTestCase(TestCase):
    """Define class for API access testing."""
    def test_forbidden_for_unauth_users(self):
        """Make sure that unauth user has no access to api urls."""
        urls = [
            '/api/',
            '/api/locks/',
            '/api/events/',
            '/api/locks/1/',
            '/api/events/1/',
            ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 403)
            response = self.client.post(url)
            self.assertEqual(response.status_code, 403)
            response = self.client.patch(url)
            self.assertEqual(response.status_code, 403)
            response = self.client.put(url)
            self.assertEqual(response.status_code, 403)
            response = self.client.delete(url)
            self.assertEqual(response.status_code, 403)
            response = self.client.head(url)
            self.assertEqual(response.status_code, 403)
            response = self.client.options(url)
            self.assertEqual(response.status_code, 403)


class APITestCase(APITestCase):
    """Define class for api testing."""
    def setUp(self):
        """Setup for testing."""
        self.user = User(username='test_user')
        self.user.save()
        self.lock = Lock(user=self.user, serial='1', name='a', location='b')
        self.lock.save()
        self.event = Event(
            lock_id=self.lock.pk,
            serial=self.lock.serial,
            mtype='manual',
            action='unlock')
        self.event.save()
        self.client.force_authenticate(user=self.user)

    def test_auth_user_has_acces_to_api_root(self):
        """Prove an auth user have access to the api urls."""
        urls = [
            '/api/',
            '/api/locks/',
            '/api/events/',
            '/api/locks/' + str(self.lock.pk) + '/',
            '/api/events/' + str(self.event.pk) + '/',
            ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_post_to_locks(self):
        """
        Prove that a Lock instance is created upon post request
        to the 'locks' api endpoint.
        """
        url = '/api/locks/'
        data = {
            'name': 'lock2',
            'location': 'home',
            'serial': '123'
        }
        # number of locks before posting to the 'locks' api endpoint
        self.assertEqual(self.user.locks.count(), 1)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # number of locks after
        self.assertEqual(self.user.locks.count(), 2)
        self.assertEqual(self.user.locks.last().name, 'lock2')
        self.assertEqual(self.user.locks.last().location, 'home')
        self.assertEqual(self.user.locks.last().serial, '123')

    def test_post_to_events(self):
        """
        Prove that an Event instance is created upon post request
        to the 'events' api endpoint.
        """
        url = '/api/events/'
        data = {
            'lock_id': self.lock.pk,
            'serial': self.lock.serial,
            'mtype': 'manual',
            'action': 'unlock'
        }
        # number of events before posting to the 'events' api endpoint
        self.assertEqual(Event.objects.all().count(), 1)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # number of locks after
        self.assertEqual(Event.objects.all().count(), 2)
        self.assertEqual(Event.objects.last().lock_id, str(self.lock.pk))
        self.assertEqual(Event.objects.last().serial, str(self.lock.serial))
        self.assertEqual(Event.objects.last().mtype, 'manual')
        self.assertEqual(Event.objects.last().action, 'unlock')
