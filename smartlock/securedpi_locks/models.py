from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class SecuredpiLock(models.Model):
    """Define class for user profile."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='locks',
        on_delete=models.CASCADE
    )
    label = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True)
    raspberry_pi_id = models.CharField(max_length=50)
    web_cam_id = models.CharField(max_length=50, blank=True)
    is_locked = models.BooleanField(default=False)

    def __str__(self):
        return 'Lock for {}'.format(self.user)
