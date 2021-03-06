from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from securedpi_locks.models import Lock
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
from securedpi_facerec.facial_recognition import facial_recognition
from securedpi.settings import FLASK_SERVER, UNCERTAINTY_THRESHOLD


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
    lock = Lock.objects.get(pk=event.lock_id)
    user_owns_lock = False
    confidence_acceptable = None

    if event.photo and lock.status == 'locked':
        dj_decision = facial_recognition.test_individual(
            event.photo.url,
            verbose=True)
        try:
            username = User.objects.get(pk=dj_decision[0]).username
            user_owns_lock = dj_decision[0] == lock.user.pk
            print('User has access to lock: ', user_owns_lock)
        except:
            print('No facial recognition made. Check if yml file exists!')
            dj_decision = ('', None)
        if dj_decision[0]:
            print('**face recognized: ', dj_decision[0], ' as member ', username)
            confidence_acceptable = dj_decision[1] < UNCERTAINTY_THRESHOLD
        elif not lock.facial_recognition:
            print('Lock does not have facial recognition enabled')

        matching_rfid = event.RFID == lock.RFID
        print('Confidence acceptable: ', confidence_acceptable, dj_decision[1])
        print('RFID matches: ', matching_rfid)

        if matching_rfid:
            if (user_owns_lock and confidence_acceptable) or not lock.facial_recognition:
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
                requests.post(FLASK_SERVER + ':5000', json=data)
                print('Request sent to Flask server.')
                return

        print('Access Denied.')
