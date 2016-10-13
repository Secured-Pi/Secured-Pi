from django.conf.urls import url, include
from securedpi_facerec import views


app_name = 'securedpi_facerec'
urlpatterns = [
    url(r'^train/$', views.upload_file, name='train'),
]


urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]
