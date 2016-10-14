from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from securedpi_locks.models import Lock
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
from securedpi_facerec import facial_recognition


@python_2_unicode_compatible
class Event(models.Model):
    """Define class for access events."""

    lock_id = models.CharField(max_length=20, blank=True)
    action = models.CharField(max_length=30, default='unlock')
    RFID = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(
        upload_to='lock_photos',
        blank=True,
        null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    serial = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='failed')
    mtype = models.CharField(max_length=20)

    def __str__(self):
        """Show event."""
        return 'Event for {}'.format(self.lock_id)


@receiver(post_save, sender=Event)
def start_FR(sender, **kwargs):
    """
    Initiate facial recognition method with received photo.

    If the photo and RFID are recognized, make post request to rasp pi to
    unlock.
    """
    event = kwargs['instance']

    if event.photo:
        dj_decision = facial_recognition.test_individual(event.photo.url, verbose=True)
        username = User.objects.get(pk=dj_decision[0]).username
        print('face recognized: ', dj_decision[0], ' as member ', username)

        lock = Lock.objects.get(pk=event.lock_id)
        user_owns_lock = dj_decision[0] == lock.user.pk
        confidence_acceptable = dj_decision[1] < 42
        matching_rfid = event.RFID == lock.RFID
        print('User has access to lock: ', user_owns_lock)
        print('Confidence acceptable: ', confidence_acceptable, dj_decision[1])
        print('RFID matches: ', matching_rfid)

        if user_owns_lock and confidence_acceptable and matching_rfid:
            serial = lock.serial
            data = {
                'event_id': event.pk,
                'action': 'unlock',
                'serial': serial,
                'mtype': 'fr'
            }
            lock.status = 'pending'
            lock.save()
            print('User authorized, sending unlock request.')
            response = requests.post('http://52.43.75.183:5000', json=data)
            return
        print('Access Denied.')
