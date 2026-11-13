from rest_framework.viewsets import ModelViewSet
from .models import Vehiculo
from .serializers import VehiculoSerializer

class VehiculoViewSet(ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']
