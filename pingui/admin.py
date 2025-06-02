from django.contrib import admin
from ..apps.cursos.models import *
from ..apps.usuarios.models import *
from ..apps.evaluaciones.models import *

admin.site.register(Administrador)
admin.site.register(Responsable)
admin.site.register(Grado)
admin.site.register(Estudiante)
admin.site.register(Docente)
admin.site.register(Materia)
admin.site.register(Tematica)
admin.site.register(Actividad)
admin.site.register(Pregunta)
admin.site.register(Calificacion)