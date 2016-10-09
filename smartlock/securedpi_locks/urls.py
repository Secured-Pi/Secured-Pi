from django.conf.urls import url
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^dashboard/',
        login_required(TemplateView.as_view(
            template_name='securedpi_locks/dashboard.html')),
        name='dashboard')
]
