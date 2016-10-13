from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from securedpi_locks.models import Lock
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
# from facial_recognition.facial_recognition import test_individual


@python_2_unicode_compatible
class Event(models.Model):
    """Define class for access events."""
    lock_id = models.CharField(max_length=20, blank=True)
    action = models.CharField(max_length=30, blank=True)
    RFID = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(
        upload_to='lock_photos',
        blank=True,
        null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    serial = models.CharField(max_length=20)
    status = models.CharField(max_length=20, blank=True)
    mtype = models.CharField(max_length=20)


    def __str__(self):
        return 'Event for {}'.format(self.lock_id)


@receiver(post_save, sender=Event)
def start_FR(sender, **kwargs):
    event = kwargs['instance']
    if event.photo:
        dj_decision = test_individual(event.photo.url)
        print('face recognized: ', dj_decision)
        lock = Lock.objects.get(pk=event.lock_id)
        if dj_decision and event.RFID == lock.RFID:
            serial = lock.serial
            data = {
                'event_id': event.pk,
                'action': 'unlock',
                'serial': serial,
                'mtype': 'fr'
                }
            lock.status = 'pending'
            lock.save()
            response = requests.post('http://52.43.75.183:5000', json=data)

        else:
            event.delete()
