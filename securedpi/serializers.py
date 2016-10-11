from rest_framework import serializers
from securedpi_locks.models import Lock
from securedpi_events.models import Event
from django.contrib.auth.models import User


class EventSerializer(serializers.ModelSerializer):
    # lock_id = serializers.ReadOnlyField(source='user.username')
    # highlight = serializers.HyperlinkedIdentityField(
    #     view_name='snippet-highlight', format='html')

    class Meta:
        model = Event
        fields = ('pk', 'lock_id', 'photo', 'method', 'action_taken',
                  'serial')


class LockSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    # highlight = serializers.HyperlinkedIdentityField(
    #     view_name='snippet-highlight', format='html')

    class Meta:
        model = Lock
        fields = ('pk', 'user', 'title', 'location', 'description',
                  'serial', 'web_cam_id', 'status',
                  'is_active', 'facial_recognition')
