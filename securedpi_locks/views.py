from django.shortcuts import render
from django.views.generic import UpdateView
from securedpi_locks.models import Lock
from securedpi_events.models import Event
import requests
import json
from django.http import HttpResponseRedirect
from django.urls import reverse


class EditLockView(UpdateView):
    """Define edit Lock class."""
    template_name = 'securedpi_locks/edit_lock.html'
    model = Lock
    fields = ['name', 'location', 'description', 'is_active', 'facial_recognition']

    # def get_form(self, form_class=None):
    #     """
    #     Modify 'photos' field in the form to show only user-specific photos.
    #     """
    #     form = super(EditAlbumView, self).get_form(form_class)
    #     qs = form.fields['photos'].queryset
    #     qs = qs.filter(user=self.request.user)
    #     form.fields['photos'].queryset = qs
    #     return form

    def get_success_url(self):
        """Set redirection after updating the album."""
        url = reverse('dashboard')
        return url


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
