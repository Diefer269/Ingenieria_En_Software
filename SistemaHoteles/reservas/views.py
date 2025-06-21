# reservas/views.py

from rest_framework import viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Reserva
from .serializers import ReservaSerializer
from .filters import ReservaFilter
from pagos.models import Pago

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all().order_by('-fecha_inicio')
    serializer_class = ReservaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ReservaFilter
    filterset_fields = ['estado', 'cliente', 'habitacion']
    search_fields = ['estado', 'cliente__nombre', 'habitacion__tipo']

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('fecha_inicio', openapi.IN_QUERY, description="Fecha mínima (YYYY-MM-DD)", type=openapi.TYPE_STRING),
            openapi.Parameter('fecha_fin', openapi.IN_QUERY, description="Fecha máxima (YYYY-MM-DD)", type=openapi.TYPE_STRING),
            openapi.Parameter('estado', openapi.IN_QUERY, description="Estado de la reserva", type=openapi.TYPE_STRING),
            openapi.Parameter('cliente', openapi.IN_QUERY, description="ID del cliente", type=openapi.TYPE_INTEGER),
            openapi.Parameter('habitacion', openapi.IN_QUERY, description="ID de la habitación", type=openapi.TYPE_INTEGER),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        tipo_pago = self.request.data.get('tipo_pago', 'Efectivo')
        reserva = serializer.save()

        # Crear el pago automáticamente
        pago = Pago.objects.create(
            monto=reserva.habitacion.precio,
            tipo_pago=tipo_pago,
            estado='exitoso'
        )

        reserva.pago = pago
        reserva.save()

        # Marcar habitación como ocupada
        reserva.habitacion.estado = 'ocupada'
        reserva.habitacion.save()

        # Enviar correo de notificación
        send_mail(
            subject='Confirmación de reserva y pago',
            message=f'Se ha registrado una reserva para la habitación "{reserva.habitacion}" '
                    f'del {reserva.fecha_inicio} al {reserva.fecha_fin}.\n'
                    f'Monto: ${pago.monto} - Tipo de pago: {pago.tipo_pago}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['jloorm2003@gmail.com', 'jloorm4@gmail.com'],
        )

    def perform_destroy(self, instance):
        habitacion = instance.habitacion
        instance.delete()
        habitacion.estado = 'disponible'
        habitacion.save()

    @action(detail=True, methods=['post'])
    def checkin(self, request, pk=None):
        reserva = self.get_object()
        if reserva.estado != 'pendiente':
            return Response({'error': 'Solo se puede hacer check-in si la reserva está pendiente.'},
                            status=status.HTTP_400_BAD_REQUEST)

        reserva.estado = 'activa'
        reserva.save()
        reserva.habitacion.estado = 'ocupada'
        reserva.habitacion.save()
        return Response({'mensaje': 'Check-in realizado correctamente.'})

    @action(detail=True, methods=['post'])
    def checkout(self, request, pk=None):
        reserva = self.get_object()
        if reserva.estado != 'activa':
            return Response({'error': 'Solo se puede hacer check-out si la reserva está activa.'},
                            status=status.HTTP_400_BAD_REQUEST)

        reserva.estado = 'finalizada'
        reserva.save()
        reserva.habitacion.estado = 'disponible'
        reserva.habitacion.save()
        return Response({'mensaje': 'Check-out realizado correctamente.'})