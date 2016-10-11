from django.shortcuts import render
from django.views.generic.base import TemplateView
from securedpi_events.models import Event


class EventView(TemplateView):
    """Establish class for Event page view."""
    template_name = 'securedpi_events/events.html'

    def get_context_data(self, **kwargs):
        context = super(EventView, self).get_context_data(**kwargs)
        all_events = Event.objects.order_by('-date_created').all()
        context['events'] = all_events
        return context
