from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.db.models.signals import post_save
from django.dispatch import receiver


@python_2_unicode_compatible
class SecuredpiProfile(models.Model):
    """Define class for user profile."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='profile',
        on_delete=models.CASCADE
    )
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=200, blank=True)
    phone_number = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return 'Profile for {}'.format(self.user)

    @property
    def is_active(self):
        return self.user.is_active

    @classmethod
    def active(cls):
        return SecuredpiProfile.objects.filter(user__is_active=True)


@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    if not SecuredpiProfile.objects.filter(user=kwargs['instance']):
        SecuredpiProfile(
            user=kwargs['instance']
        ).save()
