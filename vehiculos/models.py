from django.core.validators import MinValueValidator
from django.db import models

class Vehiculo(models.Model):
    marca = models.CharField(max_length=80)
    modelo = models.CharField(max_length=80)
    anio = models.PositiveIntegerField(validators=[MinValueValidator(1886)])
    color = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'vehiculos'
        ordering = ['id']

    def __str__(self):
        return f'{self.marca} {self.modelo} ({self.anio})'
