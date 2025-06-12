from django.core.management.base import BaseCommand
from clientes.models import Cliente
from habitaciones.models import Habitacion
from usuarios.models import Usuario
from pagos.models import Pago
from reservas.models import Reserva
from reportes.models import Reporte
from datetime import date, timedelta
from django.utils.timezone import now

class Command(BaseCommand):
    help = 'Pobla la base de datos con datos de prueba para el sistema de hoteles'

    def handle(self, *args, **kwargs):
        # 1. Crear clientes
        cliente1 = Cliente.objects.create(nombre="Luis Sánchez", documento="1100110011", email="luis@mail.com", telefono="099111222")
        cliente2 = Cliente.objects.create(nombre="Elena Torres", documento="2200220022", email="elena@mail.com", telefono="099333444")

        # 2. Crear habitaciones
        habitacion1 = Habitacion.objects.create(tipo="Suite", estado="disponible", precio=100)
        habitacion2 = Habitacion.objects.create(tipo="Doble", estado="disponible", precio=60)

        # 3. Crear usuarios
        admin = Usuario.objects.create_user(username="admin1", password="1234", rol="administrador", is_staff=True, is_superuser=True)
        recep = Usuario.objects.create_user(username="recep1", password="1234", rol="recepcionista", is_staff=True)
        gerente = Usuario.objects.create_user(username="gerente1", password="1234", rol="gerente", is_staff=True)

        # 4. Crear pagos
        pago1 = Pago.objects.create(monto=100, tipo_pago="Efectivo", estado="exitoso")
        pago2 = Pago.objects.create(monto=60, tipo_pago="Tarjeta", estado="exitoso")

        # 5. Crear reservas
        reserva1 = Reserva.objects.create(
            cliente=cliente1,
            habitacion=habitacion1,
            pago=pago1,
            fecha_inicio=date.today(),
            fecha_fin=date.today() + timedelta(days=3),
            estado="activa"
        )

        reserva2 = Reserva.objects.create(
            cliente=cliente2,
            habitacion=habitacion2,
            pago=pago2,
            fecha_inicio=date.today() + timedelta(days=1),
            fecha_fin=date.today() + timedelta(days=4),
            estado="pendiente"
        )

        # 6. Crear reportes
        Reporte.objects.create(tipo="Reservas Actuales", fecha_reporte=date.today(), usuario=gerente)
        Reporte.objects.create(tipo="Ingresos Mensuales", fecha_reporte=date.today(), usuario=admin)

        print("✔ Datos de prueba creados correctamente.")

