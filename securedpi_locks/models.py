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
    name = models.CharField(max_length=20)
    location = models.CharField(max_length=50)
    description = models.CharField(max_length=50, blank=True)
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    serial = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20, default='unlocked')
    is_active = models.BooleanField(default=False)
    facial_recognition = models.BooleanField(default=False)

    def __str__(self):
        return 'Lock for {}'.format(self.user)
