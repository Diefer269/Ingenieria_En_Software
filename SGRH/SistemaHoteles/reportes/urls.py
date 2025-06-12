from django.urls import path
from .views import ReporteReservasView, ReporteIngresosView

urlpatterns = [
    path('reservas/', ReporteReservasView.as_view()),
    path('ingresos/', ReporteIngresosView.as_view()),
]
