import uuid
from django.db import models
from ..usuarios.models import *
from ..cursos.models import *

# Create your models here.
TIPO_PREGUNTA_CHOICES = [
    ('Opción Múltiple', 'Opción Múltiple'),
    ('Verdadero/Falso', 'Verdadero/Falso'),
]

# Modelo de Actividades
class Actividad(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=100, default="Sin descripción")
    imagen = models.TextField(null=True, blank=True, default="")
    estado = models.TextField(null=False, blank=False, default="Activo")
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name="actividades", null=True, blank=True)
    tematica = models.ForeignKey(Tematica, on_delete=models.CASCADE, related_name="actividades", null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.tematica.nombre}) (Actividad)"
    
# Modelo de Preguntas
class Pregunta(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pregunta = models.TextField(max_length=50, blank=False, null=False, default="")
    imagen = models.TextField(null=False, blank=False)
    tipo = models.CharField(max_length=50, choices=TIPO_PREGUNTA_CHOICES)
    opciones_respuesta = models.TextField(null=True, blank=True, help_text="Lista de respuestas separadas por comas")
    respuesta_correcta = models.TextField(null=False, blank=False, default="")
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE, related_name="preguntas")

    def __str__(self):
        return f"Pregunta ({self.tipo}) - {self.tematica.nombre}"
    
# Modelo de Calificaciones
class Calificacion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name="calificaciones")
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE, related_name="calificaciones")
    puntaje = models.DecimalField(max_digits=2, decimal_places=1)
    notaCualitativa = models.TextField(default="")
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.estudiante.nombre} - {self.actividad.nombre}: {self.puntaje}"