from django.urls import path
from . import views

urlpatterns = [
    path('', views.calcular_accuracy, name='calcular_accuracy'),  # Nueva línea para la URL raíz
    path('calcular_accuracy/', views.calcular_accuracy, name='calcular_accuracy'),
    path('resultado_accuracy/', views.resultado_accuracy, name='resultado_accuracy'),
    # Otras rutas que puedas necesitar
]
