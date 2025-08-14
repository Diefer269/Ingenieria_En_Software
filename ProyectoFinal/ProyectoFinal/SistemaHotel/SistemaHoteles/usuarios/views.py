from rest_framework import viewsets, permissions, filters
from .models import Usuario
from .serializers import UsuarioSerializer
from rest_framework.permissions import AllowAny

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

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdminUserOnly()]
        return [permissions.AllowAny()]
        
