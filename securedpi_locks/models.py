from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Lock(models.Model):
    """Define class for user profile."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='locks',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=15)
    location = models.CharField(max_length=25)
    description = models.CharField(max_length=25, blank=True)
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    serial = models.CharField(max_length=20)
    web_cam_id = models.CharField(max_length=20, blank=True)
    status = models.CharField(
        max_length=8,
        choices=(
            ('locked', 'locked'),
            ('unlocked', 'unlocked'),
            ('pending', 'pending'),
        ),
        default='unlocked')
    is_active = models.BooleanField(default=False)
    facial_recognition = models.BooleanField(default=False)

    def __str__(self):
        return 'Lock for {}'.format(self.user)
