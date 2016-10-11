from rest_framework import serializers
from securedpi_locks.models import Lock
from django.contrib.auth.models import User


class LockSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    # highlight = serializers.HyperlinkedIdentityField(
    #     view_name='snippet-highlight', format='html')

    class Meta:
        model = Lock
        fields = ('pk', 'user', 'title', 'location', 'description',
                  'raspberry_pi_id', 'web_cam_id', 'status',
                  'is_active', 'facial_recognition')
