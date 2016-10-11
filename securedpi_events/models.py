from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from securedpi_locks.models import Lock


@python_2_unicode_compatible
class Event(models.Model):
    """Define class for access events."""
    lock_id = models.ForeignKey(
        Lock,
        related_name='events',
        on_delete=models.CASCADE
    )
    photo = models.ImageField(
        upload_to='lock_photos',
        blank=True,
        null=True)
    date_created = models.DateField(auto_now_add=True)
    serial = models.CharField(max_length=20)
    action_taken = models.CharField(
        max_length=8,
        choices=(
            ('locked', 'locked'),
            ('unlocked', 'unlocked'),
        ),
        blank=True)
    method = models.CharField(
        max_length=8,
        choices=(
            ('manual', 'manual'),
            ('fr', 'fr'),
        ),
        blank=True)


    def __str__(self):
        return 'Event for {}'.format(self.lock_id)
