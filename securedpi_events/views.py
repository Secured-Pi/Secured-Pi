from django.shortcuts import render
from django.views.generic.base import TemplateView
from securedpi_events.models import Event
from django.http import HttpResponseRedirect
from django.urls import reverse


class EventView(TemplateView):
    """Establish class for Event page view."""
    template_name = 'securedpi_events/events.html'

    def get_context_data(self, **kwargs):
        context = super(EventView, self).get_context_data(**kwargs)
        all_events = Event.objects.filter(lock_id=kwargs['pk']).order_by('-date_created')
        context['events'] = all_events
        context['lock_id'] = kwargs['pk']
        return context


def delete_old_events(request, **kwargs):
    old_events = Event.objects.filter(lock_id=kwargs['pk']).order_by('date_created')[:2]
    for event in old_events:
        event.delete()
    return HttpResponseRedirect(reverse('events', kwargs={'pk': kwargs['pk']}))
