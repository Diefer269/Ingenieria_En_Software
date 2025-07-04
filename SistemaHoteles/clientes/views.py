from rest_framework import viewsets, filters
from .models import Cliente
from .serializers import ClienteSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    """
    API para gestionar clientes: crear, listar, editar, eliminar.
    """
    queryset = Cliente.objects.all().order_by('nombre')
    serializer_class = ClienteSerializer

    # Permitir búsqueda por nombre, documento, email o teléfono
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre', 'documento', 'email', 'telefono']
