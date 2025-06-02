import uuid
from django.db.models import Subquery, OuterRef, Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import *
from django.conf import settings
from django.utils.text import slugify
from django.utils import timezone
from django.core.files.storage import default_storage
import json
import os
import shutil

# Create your views here.
#*Profesores -> Actividades
def professor_actividades(request):
    # Filtrar actividades activas
    actividades_activas = Actividad.objects.filter(estado="Activo")
    materias_con_actividades = []

    # Obtener todas las materias que tienen al menos una actividad
    materias = Materia.objects.all()
    for materia in materias:
        actividades_materia = actividades_activas.filter(materia=materia)
        if actividades_materia.exists():
            materias_con_actividades.append({
                'materia': materia,
                'actividades': actividades_materia
            })

    # Filtrar actividades archivadas
    actividades_archivadas = Actividad.objects.filter(estado="Archivada")

    return render(request, 'profesores/actividades/actividades.html', {
        'materias_con_actividades': materias_con_actividades,
        'actividades_archivadas': actividades_archivadas
    })

#*Profesores -> Vista de Actividades para crear
def professor_crear_actividad(request):
    listarMaterias = Materia.objects.all()
    listarTematicas = Tematica.objects.all()
    return render(request, 'profesores/actividades/viewActivity.html', {'Materia':listarMaterias, 'Tematica': listarTematicas})

#*Profesores -> Vista de Actividades para Editar
def professor_visualizar_actividad(request, id):
    actividad = get_object_or_404(Actividad, id=id)  # Obtiene la actividad
    preguntas = Pregunta.objects.filter(actividad_id=id) # Obtiene las preguntas de la actividad
    listarMaterias = Materia.objects.all()
    listarTematicas = Tematica.objects.all()
    tematicas_materia_seleccionada = Tematica.objects.filter(materia=actividad.materia)

    for p in preguntas:
        if p.opciones_respuesta:  # Asegura que no sea None
            p.opciones_list = p.opciones_respuesta.split(',')  # crea una lista con las 4 opciones

    return render(request, 'profesores/actividades/viewActivity.html', {'Actividad': actividad, 'Pregunta': preguntas, 'Materia':listarMaterias, 'Tematica': listarTematicas, 'TematicaSeleccionadas': tematicas_materia_seleccionada})

def obtener_tematicas_asociadas(request):
    materia_id = request.GET.get('materia_id')
    tematicas = Tematica.objects.filter(materia_id=materia_id).values('id', 'nombre')
    return JsonResponse(list(tematicas), safe=False)

#*Profesores -> Crear actividad
def createActivity(request):
    if request.method == 'POST':
        # Obtener y parsear los datos
        data_json = request.POST.get("actividad")

        data = json.loads(data_json)
        nombre_actividad = data.get("nombre")
        descripcion_actividad = data.get("descripcion")
        materia_actividad = data.get("materia")
        tematica_actividad = data.get("tematica")
        preguntas = data.get("preguntas", [])

        # Crear carpeta de destino
        folder_name = slugify(nombre_actividad)
        base_path = os.path.join(settings.BASE_DIR, 'pingui', 'static', 'assets', 'activities', 'assets', folder_name)
        os.makedirs(base_path, exist_ok=True)

        # Guardar imagen principal
        imagen_actividad = request.FILES.get("imagenActividad")
        nombre_archivo_thumbnail = None

        if imagen_actividad:
            # Definimos el nombre con prefijo (puedes agregar un UUID o timestamp para evitar colisiones)
            nombre_archivo_thumbnail = "imagen_actividad_" + imagen_actividad.name  
            ruta_actividad = os.path.join(settings.BASE_DIR, "pingui", "static", "assets", "activities", "thumbnails", nombre_archivo_thumbnail)  # Aquí agregas la carpeta thumbnails

            with default_storage.open(ruta_actividad, 'wb+') as f:
                for chunk in imagen_actividad.chunks():
                    f.write(chunk)

        ruta_relativa_thumbnail = f"activities/thumbnails/{nombre_archivo_thumbnail}"

        # Obtener la referencia de la materia y tematica
        materia = get_object_or_404(Materia, id=materia_actividad)
        tematica = get_object_or_404(Tematica, id=tematica_actividad)

        actividad = Actividad.objects.create(
            id=uuid.uuid4(),
            nombre=nombre_actividad,
            descripcion=descripcion_actividad,
            imagen=ruta_relativa_thumbnail,
            materia=materia,
            tematica=tematica
        )

        # Insertar cada pregunta a la base de datos y ademas su imagen
        for i, pregunta in enumerate(preguntas):
            key = f"imagenPregunta_{i}"
            id_pregunta = uuid.uuid4()

            imagen_pregunta = request.FILES.get(key)
            if imagen_pregunta:
                nombre_archivo = f"{id_pregunta}_" + imagen_pregunta.name
                ruta_pregunta = os.path.join(base_path, nombre_archivo)
                with default_storage.open(ruta_pregunta, 'wb+') as f:
                    for chunk in imagen_pregunta.chunks():
                        f.write(chunk)

            # Obtener datos de la pregunta
            tipo = pregunta.get("tipoPregunta")
            texto = pregunta.get("pregunta")
            respuesta = pregunta.get("respuesta")
            opciones_unidas = ""

            if tipo == "seleccion_multiple":
                opcion1 = pregunta.get("opcion_a")
                opcion2 = pregunta.get("opcion_b")
                opcion3 = pregunta.get("opcion_c")
                opcion4 = pregunta.get("opcion_d")
                opciones_unidas = f"{opcion1},{opcion2},{opcion3},{opcion4}"

            ruta_relativa_asset = f"activities/assets/{folder_name}/{nombre_archivo}"

            pregunta = Pregunta.objects.create(
                id=id_pregunta,
                pregunta=texto,
                imagen=ruta_relativa_asset,
                tipo=tipo,
                opciones_respuesta=opciones_unidas,
                respuesta_correcta=respuesta,
                actividad=actividad
            )
        
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})

#*Profesores -> Editar actividad
def editActivity(request):
    if request.method == 'POST':
        # Obtener y parsear los datos
        data_json = request.POST.get("actividad")

        data = json.loads(data_json)
        id_actividad = data.get("id")
        nombre_actividad = data.get("nombre")
        descripcion_actividad = data.get("descripcion")
        materia_actividad = data.get("materia")
        tematica_actividad = data.get("tematica")
        preguntas = data.get("preguntas", [])

        actividad = Actividad.objects.get(id=id_actividad)

        # Obtener el nombre anterior y el nuevo
        nombre_anterior = actividad.nombre
        folder_name_nuevo = slugify(nombre_actividad)
        folder_name_anterior = slugify(nombre_anterior)
        folder_name = folder_name_anterior

        ruta_base_actividades = os.path.join(settings.BASE_DIR, 'pingui', 'static', 'assets', 'activities', 'assets')
        ruta_anterior = os.path.join(ruta_base_actividades, folder_name_anterior)
        ruta_nueva = os.path.join(ruta_base_actividades, folder_name_nuevo)

        # Si el nombre cambió y la carpeta anterior existe, renombrarla
        if folder_name_anterior != folder_name_nuevo and os.path.exists(ruta_anterior):
            os.rename(ruta_anterior, ruta_nueva)

            # Actualizar rutas de imagen de preguntas
            preguntas_con_imagen = Pregunta.objects.filter(actividad=actividad)
            for pregunta in preguntas_con_imagen:
                if pregunta.imagen:
                    # Reemplaza solo el nombre de carpeta en la ruta relativa
                    pregunta.imagen = pregunta.imagen.replace(folder_name_anterior, folder_name_nuevo)
                    pregunta.save()

            folder_name = folder_name_nuevo

        # Usar ruta_nueva como base_path
        base_path = ruta_nueva

        # Verificar si se subió una nueva imagen
        imagen_actividad = request.FILES.get("imagenActividad")
        nombre_archivo_thumbnail = None

        if imagen_actividad:
            # Eliminar imagen anterior si existe
            if actividad.imagen and default_storage.exists(os.path.join(settings.BASE_DIR, 'pingui', 'static', 'assets', actividad.imagen)):
                ruta_anterior = os.path.join(settings.BASE_DIR, 'pingui', 'static', 'assets', actividad.imagen)
                default_storage.delete(ruta_anterior)

            # Guardar la nueva imagen
            nombre_archivo_thumbnail = "imagen_actividad_" + imagen_actividad.name
            ruta_actividad = os.path.join(settings.BASE_DIR, "pingui", "static", "assets", "activities", "thumbnails", nombre_archivo_thumbnail)

            with default_storage.open(ruta_actividad, 'wb+') as f:
                for chunk in imagen_actividad.chunks():
                    f.write(chunk)

            ruta_relativa_thumbnail = f"activities/thumbnails/{nombre_archivo_thumbnail}"
            actividad.imagen = ruta_relativa_thumbnail  # Actualizar campo imagen

        # Obtener la referencia de la materia y tematica
        materia = get_object_or_404(Materia, id=materia_actividad)
        tematica = get_object_or_404(Tematica, id=tematica_actividad)

        # Actualizar otros campos
        actividad.nombre = nombre_actividad
        actividad.descripcion = descripcion_actividad
        actividad.materia = materia
        actividad.tematica = tematica
        actividad.save()

        # PREGUNTAS

        """
        Si la pregunta tiene id, se actualiza:
            Si trae nueva imagen: reemplaza la imagen anterior.
            Si no trae imagen: conserva la anterior.

        Si no tiene id, se crea una nueva:
            Obligatoriamente debe tener imagen.
        """

        # Paso previo: obtener todos los IDs de preguntas ya registradas para esta actividad
        preguntas_existentes_ids = set(Pregunta.objects.filter(actividad=actividad).values_list('id', flat=True))

        # IDs de las preguntas enviadas (las que deben mantenerse o actualizarse)
        preguntas_enviadas_ids = set()

        for i, pregunta_data in enumerate(preguntas):
            key = f"imagenPregunta_{i}"
            imagen_pregunta = request.FILES.get(key)
            pregunta_id = pregunta_data.get("id")

            tipo = pregunta_data.get("tipoPregunta")
            texto = pregunta_data.get("pregunta")
            respuesta = pregunta_data.get("respuesta")
            opciones_unidas = ""

            if tipo == "seleccion_multiple":
                opcion1 = pregunta_data.get("opcion_a")
                opcion2 = pregunta_data.get("opcion_b")
                opcion3 = pregunta_data.get("opcion_c")
                opcion4 = pregunta_data.get("opcion_d")
                opciones_unidas = f"{opcion1},{opcion2},{opcion3},{opcion4}"

            if pregunta_id != None:
                pregunta_uuid = uuid.UUID(pregunta_id)
                preguntas_enviadas_ids.add(pregunta_uuid)
                pregunta_existente = Pregunta.objects.get(id=pregunta_id)

                # Si se subió una nueva imagen, se reemplaza
                if imagen_pregunta:
                    # Eliminar imagen anterior si existe
                    if pregunta_existente.imagen:
                        ruta_anterior = os.path.join(settings.BASE_DIR, 'pingui', 'static', 'assets', pregunta_existente.imagen)
                        default_storage.delete(ruta_anterior)

                    nombre_archivo = f"{pregunta_id}_" + imagen_pregunta.name
                    ruta_pregunta = os.path.join(base_path, nombre_archivo)
                    with default_storage.open(ruta_pregunta, 'wb+') as f:
                        for chunk in imagen_pregunta.chunks():
                            f.write(chunk)

                    ruta_relativa = f"activities/assets/{folder_name}/{nombre_archivo}"
                    pregunta_existente.imagen = ruta_relativa

                # Actualizar campos
                pregunta_existente.pregunta = texto
                pregunta_existente.tipo = tipo
                pregunta_existente.respuesta_correcta = respuesta
                pregunta_existente.opciones_respuesta = opciones_unidas
                pregunta_existente.save()
            else:
                if imagen_pregunta:
                    id_nueva_pregunta = uuid.uuid4()

                    nombre_archivo = f"{id_nueva_pregunta}_" + imagen_pregunta.name
                    ruta_pregunta = os.path.join(base_path, nombre_archivo)
                    with default_storage.open(ruta_pregunta, 'wb+') as f:
                        for chunk in imagen_pregunta.chunks():
                            f.write(chunk)

                    ruta_relativa = f"activities/assets/{folder_name}/{nombre_archivo}"

                    Pregunta.objects.create(
                        id=id_nueva_pregunta,
                        pregunta=texto,
                        imagen=ruta_relativa,
                        tipo=tipo,
                        opciones_respuesta=opciones_unidas,
                        respuesta_correcta=respuesta,
                        actividad=actividad
                    )

        # Eliminar preguntas que ya no están en el frontend
        preguntas_para_eliminar = preguntas_existentes_ids - preguntas_enviadas_ids

        for pregunta_id_eliminar in preguntas_para_eliminar:
            pregunta = Pregunta.objects.get(id=pregunta_id_eliminar)
            if pregunta.imagen:
                # Ruta absoluta al archivo real en disco
                ruta_imagen = os.path.join(settings.BASE_DIR, 'pingui', 'static', 'assets', pregunta.imagen)
                if default_storage.exists(ruta_imagen):
                    default_storage.delete(ruta_imagen)

        Pregunta.objects.filter(id__in=preguntas_para_eliminar).delete()
        
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})

#*Profesores -> Eliminar Actividad
def deleteActivity(request, id):
    actividad = get_object_or_404(Actividad, id=id)  # Usa get_object_or_404 para evitar errores si no existe
    
    # 1. Eliminar thumbnail anterior    
    thumbnail_path = os.path.join(settings.BASE_DIR, 'pingui', 'static', 'assets', actividad.imagen)
    if os.path.exists(thumbnail_path):
        os.remove(thumbnail_path)

    # 2. Eliminar carpeta de imagenes de preguntas con shutil para evitar eliminar una por una
    
    # Convertir el nombre a minúsculas y reemplazar espacios por guiones
    folder_name = actividad.nombre.lower().replace(" ", "-")

    # Ruta a la carpeta de assets
    assets_folder = os.path.join(settings.BASE_DIR, 'pingui', 'static', 'assets', 'activities', 'assets', folder_name)

    if os.path.exists(assets_folder):
        shutil.rmtree(assets_folder)

     # 2. Eliminar la actividad de la base de datos
    actividad.delete() 
    return JsonResponse({"success": True})    

#*Profesores -> Archivar Actividad
def archiveActivity(request, id):
    actividad = get_object_or_404(Actividad, id=id)  # Usa get_object_or_404 para evitar errores si no existe
    
    if actividad.estado == "Archivada":
        actividad.estado = "Activo"
        mensaje = "desarchivada"
    else:
        actividad.estado = "Archivada"
        mensaje = "archivada"

    actividad.save()
    return JsonResponse({"success": True, "accion": mensaje})

#*Estudiantes -> Actividades
def student_activities_view(request):
    materias = Materia.objects.all()
    materias_con_actividades = []

    for materia in materias:
        tiene_actividades_activas = Actividad.objects.filter(estado="Activo", materia=materia).exists()
        if tiene_actividades_activas:
            materias_con_actividades.append(materia)

    return render(request, 'estudiantes/learning/learning.html', {
        'materias': materias_con_actividades,
        'materia_inicial_id': materias_con_actividades[0].id if materias_con_actividades else None
    })

from django.http import JsonResponse

def actividades_por_materia(request, materia_id):
    documento_estudiante = request.session['Documento']
    
    #Se obtiene el numero de pagina
    pagina = int(request.GET.get("pagina", 1))
    por_pagina = 5
    inicio = (pagina - 1) * por_pagina
    fin = inicio + por_pagina

    materia = Materia.objects.get(id=materia_id)
    actividades_info = obtener_actividades_de_materia(materia, documento_estudiante)
    actividades_pagina = actividades_info[inicio:fin]
    hay_mas = len(actividades_info) > fin

    return JsonResponse({'actividades': actividades_pagina, 'hay_mas': hay_mas})

def obtener_actividades_de_materia(materia, documento_estudiante):
    actividades_activas = Actividad.objects.filter(estado="Activo", materia=materia)
    actividades_info = []

    for actividad in actividades_activas:
        completada = Calificacion.objects.filter(
            estudiante_id=documento_estudiante,
            actividad_id=actividad.id
        ).exists()

        actividades_info.append({
            'id': actividad.id,
            'nombre': actividad.nombre,
            'descripcion': actividad.descripcion,
            'thumbnail': actividad.imagen,
            'tematica': actividad.tematica.nombre,
            'estado': 'complete' if completada else 'pending'
        })

    return actividades_info

#Estudiantes -> Realizar actividad
def iniciar_actividad(request, actividad_id):
    actividad = Actividad.objects.get(id=actividad_id)
    return render(request, 'estudiantes/learning/practica.html', {
        'actividad': actividad
    })

def get_questions_count(request, actividad_id):
    actividad = Actividad.objects.get(id=actividad_id)

    # Obtener todas las preguntas asociadas a esta actividad
    total_preguntas = Pregunta.objects.filter(actividad_id=actividad).count()

    return JsonResponse({
        'total_preguntas': total_preguntas
    })

def cargar_pregunta(request, actividad_id, numero):
    actividad = Actividad.objects.get(id=actividad_id)

    # Obtener todas las preguntas
    preguntas = list(Pregunta.objects.filter(actividad_id=actividad))
    pregunta = preguntas[int(numero) - 1]

    return JsonResponse({
        'id': pregunta.id,
        'texto': pregunta.pregunta,
        'imagen': pregunta.imagen,
        'tipo': pregunta.tipo,
        'opciones': pregunta.opciones_respuesta,
        'respuesta_correcta': pregunta.respuesta_correcta
    })

#* Estudiante -> Insertar calificación

def insert_grade(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            documento = request.session.get('Documento')

            estudiante = Estudiante.objects.get(documento=documento)
            actividad = Actividad.objects.get(id=data['actividad_id'])
            puntaje = float(data['puntaje'])
            nota_cualitativa = data['notaCualitativa']
            fecha_actual = timezone.now()

            calificacion = Calificacion.objects.create(
                id=uuid.uuid4(),
                estudiante=estudiante,
                actividad=actividad,
                puntaje=puntaje,
                notaCualitativa=nota_cualitativa,
                fecha_hora=fecha_actual
            )
        
            return JsonResponse({'mensaje': 'Calificación registrada correctamente.'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
#* Estudiante -> Ver intentos
def student_tries(request, actividad_id):
    documento = request.session.get('Documento')
    
    # Filtrar por el documento del estudiante y el ID de la actividad
    listar = Calificacion.objects.filter(
        actividad_id=actividad_id,
        estudiante_id=documento
    )

    actividad = Actividad.objects.get(id=actividad_id).nombre

    return render(request, 'estudiantes/learning/intentos.html', {'Intentos':listar, 'Actividad': actividad})

#* Profesor -> Ver Notas
def professor_grades(request, actividad_id):  
    UMBRAL_APROBACION = 3.0

    # Subconsulta: obtener el puntaje máximo por estudiante
    max_puntajes = Calificacion.objects.filter(
        actividad_id=actividad_id,
        estudiante_id=OuterRef('estudiante_id')
    ).order_by('-puntaje').values('puntaje')[:1]

    # Obtener los registros con el máximo puntaje por estudiante
    mejores_intentos = Calificacion.objects.filter(
        actividad_id=actividad_id,
        puntaje=Subquery(max_puntajes)
    ).order_by('-puntaje')

    # Contar aprobados y desaprobados con base en el puntaje
    aprobados = mejores_intentos.filter(puntaje__gte=UMBRAL_APROBACION).count()
    desaprobados = mejores_intentos.filter(puntaje__lt=UMBRAL_APROBACION).count()

    # Cargar nombre de la actividad
    actividad = Actividad.objects.get(id=actividad_id).nombre

    return render(request, 'profesores/actividades/calificaciones.html', {
        'Intentos': mejores_intentos,
        'Actividad': actividad,
        'aprobados': aprobados,
        'desaprobados': desaprobados
    })