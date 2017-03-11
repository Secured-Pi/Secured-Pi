from rest_framework import serializers
from securedpi_locks.models import Lock
from securedpi_events.models import Event


class EventSerializer(serializers.ModelSerializer):
    """Define class to serialize events."""

    class Meta:
        model = Event
        fields = ('pk', 'lock_id', 'photo', 'mtype', 'status',
                  'serial', 'action', 'RFID', 'date_created')


class LockSerializer(serializers.ModelSerializer):
    """Define class to serialize locks."""

    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Lock
        fields = ('pk', 'user', 'name', 'location', 'description',
                  'serial', 'status', 'is_active', 'facial_recognition',
                  'date_created', 'date_modified', 'RFID')
