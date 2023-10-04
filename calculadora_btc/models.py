# calculadora_btc/models.py
from django.db import models

class DatosHistoricos(models.Model):
    fecha = models.DateField()
    precio_cierre = models.FloatField()

    def __str__(self):
        return f"{self.fecha} - ${self.precio_cierre}"
