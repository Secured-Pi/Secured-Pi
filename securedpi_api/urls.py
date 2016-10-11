from rest_framework.routers import DefaultRouter
from securedpi_api import views


router = DefaultRouter()
router.register(r'locks', views.LockViewSet)
router.register(r'events', views.EventViewSet)
