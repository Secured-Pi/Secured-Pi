from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from securedpi_locks import views



urlpatterns = [
    url(r'^(?P<pk>\d+)/edit/$',
        login_required(views.EditLockView.as_view()),
        name='edit_lock'),
    url(r'^(?P<pk>\d+)/delete/$',
        login_required(views.DeleteLockView.as_view()),
        name='delete_lock'),
    url(r'^manual-unlock/(?P<pk>\d+)/$',
        login_required(views.manual_action),
        kwargs={'action': 'unlock'},
        name='manual_unlock'),
    url(r'^manual-lock/(?P<pk>\d+)/$',
        login_required(views.manual_action),
        kwargs={'action': 'lock'},
        name='manual_lock'),
]


urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]
