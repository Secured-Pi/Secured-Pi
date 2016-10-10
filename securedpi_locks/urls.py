from django.conf.urls import url, include
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter
from securedpi_locks import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'locks', views.LockViewSet)

urlpatterns = [
    url(r'^dashboard/',
        login_required(views.DashboardView.as_view()),
        name='dashboard')
]


urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]
