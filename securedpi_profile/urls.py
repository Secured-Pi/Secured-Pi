from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from securedpi_profile import views
from django.views.generic.base import TemplateView



urlpatterns = [
    url(r'^$',
        login_required(TemplateView.as_view(
            template_name='securedpi_profile/profile.html'
        )),
        name='profile'),
    url(r'^(?P<pk>\d+)/edit/$',
        login_required(views.EditProfileView.as_view()),
        name='edit_profile'),
]
