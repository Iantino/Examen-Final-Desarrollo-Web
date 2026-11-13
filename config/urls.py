from django.urls import include, path
from rest_framework.routers import DefaultRouter
from vehiculos.views import VehiculoViewSet

router = DefaultRouter()
router.register('vehiculos', VehiculoViewSet, basename='vehiculo')

urlpatterns = [path('api/', include(router.urls))]
