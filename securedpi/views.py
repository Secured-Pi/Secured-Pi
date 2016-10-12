from django.shortcuts import render
from django.views.generic import TemplateView


class DashboardView(TemplateView):
    """Establish class for Dashboard page view."""
    template_name = 'securedpi/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        current_user = self.request.user
        locks_by_created_date = current_user.locks.order_by('-date_created')
        context['locks'] = locks_by_created_date
        return context
