"""securedpi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from securedpi_api.urls import router
from django.contrib.auth.decorators import login_required
from securedpi.views import DashboardView


urlpatterns = [
    url(r'^admin/',
        admin.site.urls),
    url(r'^$',
        TemplateView.as_view(
            template_name='securedpi/home_page.html'),
        name='homepage'),
    url(r'^dashboard/',
        login_required(DashboardView.as_view()),
        name='dashboard'),
    url(r'^accounts/',
        include('registration.backends.hmac.urls')),
    url(r'^about/$',
        TemplateView.as_view(template_name='securedpi/about_page.html'),
        name='about'),
    url(r'^locks/',
        include('securedpi_locks.urls')),
    url(r'^events/',
        include('securedpi_events.urls')),
    # url(r'^profile',
    #     include('securedpi_profile.urls')),
]

urlpatterns += [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
        )
