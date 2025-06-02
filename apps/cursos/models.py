import uuid
from django.db import models
from ..usuarios.models import *

# Create your models here.
# Modelo de Materias
class Materia(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.nombre} (Materia)"

# Modelo de Temáticas
class Tematica(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    materia = models.ForeignKey(Materia, on_delete=models.SET_NULL, null=True, related_name="tematicas")

    def __str__(self):
        return f"{self.nombre} ({self.materia.nombre} - {self.grado.nombre}) (Temática)"
    