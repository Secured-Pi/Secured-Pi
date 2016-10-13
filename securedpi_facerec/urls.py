from django.conf.urls import url, include
from securedpi_facerec import views


urlpatterns = [
    url(r'^photos/$', views.PhotoView.as_view(), name='training_photos'),
    url(r'^train/$', views.TrainingView.as_view(), name='training'),
]


urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]
