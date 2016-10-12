from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from securedpi_locks.models import Lock
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
# from facial_recognition.facial_recognition import test_individual
import json


@python_2_unicode_compatible
class Event(models.Model):
    """Define class for access events."""
    lock_id = models.CharField(max_length=20, blank=True)
    action = models.CharField(max_length=30, blank=True)
    RFID = models.CharField(max_length=20, blank=True)
    photo = models.ImageField(
        upload_to='lock_photos',
        blank=True,
        null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    serial = models.CharField(max_length=20)
    action_taken = models.CharField(max_length=20, blank=True)
    mtype = models.CharField(max_length=20)


    def __str__(self):
        return 'Event for {}'.format(self.lock_id)


# @receiver(post_save, sender=Event)
# def start_FR(sender, **kwargs):
#     event = kwargs['instance']
#     if event.photo:
#         dj_decision = test_individual(event.photo.url)
#         if dj_decision:
#             serial = '00000000cfef42b5'
#             token = 'test-token'
#             data = json.dumps(
#                 {'action': 'unlock',
#                  'serial': serial,
#                  'token': token,
#                  'type': 'fr'
#                  }
#                 )
#             headers = {'content-type': 'application/json'}
#             response = requests.post('http://52.43.75.183:5000', data=data, headers=headers)
