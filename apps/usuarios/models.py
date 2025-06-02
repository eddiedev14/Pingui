import uuid
from django.db import models

# Create your models here.

# Definición de choices como listas
SEXO_CHOICES = [
    ('M', 'Masculino'),
    ('F', 'Femenino'),
    ('O', 'Otro')
]

# Modelo de Administradores

# Modelo de Responsables (Padres o Tutores)
class Responsable(models.Model):
    documento = models.CharField(primary_key=True, max_length=10)  
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nombre} {self.apellido} (Responsable)"

# Modelo de Estudiantes
class Estudiante(models.Model):
    documento = models.CharField(primary_key=True, max_length=10)
    nombre = models.CharField(max_length=100)
    responsable = models.ForeignKey(Responsable, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} (Estudiante)"
    
# Modelo de Docentes
class Docente(models.Model):
    documento = models.CharField(primary_key=True, max_length=10)
    nombre = models.CharField(max_length=100)
    correo = models.CharField(max_length=100, unique=True)
    contraseña = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} {self.apellido} (Docente)"