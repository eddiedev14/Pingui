from . import views
from django.urls import path

urlpatterns = [
    #*Profesores -> Materias
    path('profesores/materias/', views.professor_materias),
    path('profesores/materias/agregar/', views.add_materias),
    path('profesores/materias/createMateria/', views.createMateria),
    path('profesores/materias/editar/<id>/', views.edit_materias),
    path('profesores/materias/updateMateria/<id>/', views.updateMateria),
    path('profesores/materias/deleteMateria/<id>/', views.deleteMateria),

    #*Profesores -> Materias
    path('profesores/tematicas/', views.professor_tematicas),
    path('profesores/tematicas/agregar/', views.add_tematicas),
    path('profesores/tematicas/createTematica/', views.createTematica),
    path('profesores/tematicas/editar/<id>/', views.edit_tematicas),
    path('profesores/tematicas/updateTematica/<id>/', views.updateTematica),
    path('profesores/tematicas/deleteTematica/<id>/', views.deleteTematica),
]
