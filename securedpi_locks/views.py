from django.shortcuts import render
from django.views.generic import TemplateView
from securedpi_locks.models import Lock
from securedpi_events.models import Event
import requests
import json


def manual_action(request, **kwargs):
    if request.method == 'GET':
        #serial = '00000000cfef42b5'
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
        locks = Lock.objects.filter(user=request.user).all()
        #import pdb; pdb.set_trace()
        #response = requests.post('http://52.43.75.183:5000', json=data)
    return render(request, 'securedpi/dashboard.html', {'locks': locks})
