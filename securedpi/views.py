from django.shortcuts import render
from django.views.generic import TemplateView


class DashboardView(TemplateView):
    """Establish class for Dashboard page view."""
    template_name = 'securedpi/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        locks = self.request.user.locks.order_by('pk')
        context['locks'] = locks
        return context
