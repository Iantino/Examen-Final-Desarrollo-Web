from django.urls import include, path
from django.http import FileResponse
from django.conf import settings
from rest_framework.routers import DefaultRouter
from vehiculos.views import VehiculoViewSet

router = DefaultRouter()
router.register('vehiculos', VehiculoViewSet, basename='vehiculo')

def consola(request):
    return FileResponse(open(settings.BASE_DIR / 'herramientas' / 'cliente-http.html', 'rb'), content_type='text/html')

urlpatterns = [path('api/', include(router.urls)), path('', consola)]
