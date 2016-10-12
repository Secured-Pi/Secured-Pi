from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Photo(models.Model):
    title = models.CharField(
            max_length=128,
            blank=True,
            null=True
    )
    description = models.CharField(
            max_length=500,
            blank=True,
            null=True
    )
    date_uploaded = models.DateTimeField(
            auto_now_add=True,
            null=False)
    date_modified = models.DateTimeField(null=True)
    image = models.ImageField(upload_to='images/%Y-%m-%d')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return "{}: {}".format(self.title, self.user.username)
