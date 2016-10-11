from django.conf.urls import url, include
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter
from securedpi_locks import views
from securedpi_locks.models import Lock

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'locks', views.LockViewSet)

urlpatterns = [
    url(r'^dashboard/',
        login_required(views.DashboardView.as_view()),
        name='dashboard'),
    # url(r'^(?P<pk>\d+)/$',
    #     login_required(DetailView.as_view(
    #         template_name='securedpi_locks/lock_details.html',
    #         model=Lock,
    #         context_object_name='lock'
    #     )),
    #     name='lock_details'),
    url(r'^manual/unlock/',
        login_required(views.manual_unlock),
        name='manual_unlock'),
    url(r'^manual/lock/',
        login_required(views.manual_lock),
        name='manual_lock'),
    url(r'^update-status/',
        login_required(views.update_status),
        name='update_status'),
]


urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]
