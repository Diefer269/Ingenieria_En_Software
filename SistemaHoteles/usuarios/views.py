from rest_framework import viewsets, permissions, filters
from .models import Usuario
from .serializers import UsuarioSerializer

class IsAdminUserOnly(permissions.BasePermission):
    """
    Permite acceso solo a usuarios con rol 'administrador'.
    """
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and (user.is_superuser or getattr(user, 'rol', None) == 'administrador'))

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all().order_by('username')
    serializer_class = UsuarioSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'first_name', 'last_name', 'email', 'rol']
    ordering_fields = ['username', 'rol']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUserOnly()]
        return [permissions.AllowAny()]
        
