from django.shortcuts import render
from django.views.generic import TemplateView
from securedpi_locks.models import Lock
from securedpi_events.models import Event
import requests
import json
from django.http import HttpResponseRedirect
from django.urls import reverse


def manual_action(request, **kwargs):
    lock = Lock.objects.get(pk=kwargs['pk'])
    data = {
        'lock_id': kwargs['pk'],
        'action': kwargs['action'],
        'serial': lock.serial,
        'mtype': 'manual'
        }
    new_event = Event(**data)
    new_event.save()
    data['event_id'] = new_event.pk
    lock.status = 'pending'
    lock.save()
    response = requests.post('http://52.43.75.183:5000', json=data)
    return HttpResponseRedirect(reverse('dashboard'))
