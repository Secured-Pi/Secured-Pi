from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Photo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    date_uploaded = models.DateTimeField(
            auto_now_add=True,
            null=False)
    image = models.ImageField(upload_to='training')

    def __str__(self):
        return "Photo: {}".format(self.user.username)
