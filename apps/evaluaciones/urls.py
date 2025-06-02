from . import views
from django.urls import path

urlpatterns = [
    #*Profesores -> Actividades
    path('profesores/actividades/', views.professor_actividades),
    path('profesores/actividades/view/', views.professor_crear_actividad),
    path('profesores/actividades/view/<id>/', views.professor_visualizar_actividad),
    path('obtener-tematicas/', views.obtener_tematicas_asociadas),
    path('profesores/actividades/create/', views.createActivity),
    path('profesores/actividades/edit/', views.editActivity),
    path('profesores/actividades/delete/<id>', views.deleteActivity),
    path('profesores/actividades/archive/<id>', views.archiveActivity),

    #*Profesores -> Calificaciones
    path('profesores/actividades/calificaciones/<actividad_id>/', views.professor_grades),

    #*Estudiantes -> Actividades
    path('estudiantes/actividades/', views.student_activities_view),
    path('estudiantes/actividades/<materia_id>/', views.actividades_por_materia),
    path('estudiantes/actividades/<actividad_id>/iniciar/', views.iniciar_actividad),
    path('estudiantes/actividades/<actividad_id>/getQuestionsCount/', views.get_questions_count),
    path('estudiantes/actividades/<actividad_id>/pregunta/<numero>/', views.cargar_pregunta),
    
    #*Estudiantes -> Intentos
    path('estudiantes/insertarCalificacion/', views.insert_grade),
    path('estudiantes/actividades/<actividad_id>/intentos/', views.student_tries),
]