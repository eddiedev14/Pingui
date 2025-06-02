import uuid
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import *

# Create your views here.
#*Profesores -> Materias
def professor_materias(request):
    listar = Materia.objects.all()
    return render(request, 'profesores/materias/materias.html', {'Materia':listar})

def add_materias(request):
    return render(request, 'profesores/materias/agregarMateria.html')

def edit_materias(request, id):
    materia = get_object_or_404(Materia, id=id)  # Obtiene el grado específico
    data = {'id': id, 'nombre': materia.nombre}  # Crea un diccionario con los datos
    return render(request, 'profesores/materias/editarMateria.html', {'data':data})

def createMateria(request):
    if request.method == 'POST':
        nombre = request.POST['materia']

        materia = Materia.objects.create(
            id=uuid.uuid4(),
            nombre = nombre,
        )

        return redirect('/profesores/materias/?message=La%20materia%20ha%20sido%20creado%20correctamente')

def updateMateria(request, id):
    if request.method == 'POST':
        materia = Materia.objects.get(id=id)
        nombre = request.POST['materia']
        materia.nombre = nombre
        materia.save()
        return redirect('/profesores/materias/?message=La%20materia%20ha%20sido%20actualizada%20correctamente')  
    
def deleteMateria(request, id):
    materia = get_object_or_404(Materia, id=id)  # Usa get_object_or_404 para evitar errores si no existe
    materia.delete()
    return redirect('/profesores/materias/?message=La%20materia%20ha%20sido%20eliminada%20correctamente')

#*Profesores -> Tematicas
def professor_tematicas(request):
    listar = Tematica.objects.all()
    return render(request, 'profesores/tematicas/tematicas.html', {'Tematica':listar})

def add_tematicas(request):
    listar = Materia.objects.all()
    return render(request, 'profesores/tematicas/agregarTematica.html', {'Materia':listar})

def edit_tematicas(request, id):
    tematica = get_object_or_404(Tematica, id=id)  # Obtiene el grado específico
    listar = Materia.objects.all()
    data = {'id': id, 'nombre': tematica.nombre, 'descripcion': tematica.descripcion, 'materia': tematica.materia.id, 'materias': listar}  # Crea un diccionario con los datos
    return render(request, 'profesores/tematicas/editarTematica.html', {'data':data})

def createTematica(request):
    if request.method == 'POST':
        nombre = request.POST['tematica']
        descripcion = request.POST['descripcion']
        materia_id = request.POST['materia']

        # Obtener la referencia de la materia en lugar de crear una nueva
        materia = get_object_or_404(Materia, id=materia_id)

        tematica = Tematica.objects.create(
            id=uuid.uuid4(),
            nombre=nombre,
            descripcion=descripcion,
            materia=materia
        )

        return redirect('/profesores/tematicas/?message=La%20tematica%20ha%20sido%20creada%20correctamente')

def updateTematica(request, id):
    if request.method == 'POST':
        tematica = Tematica.objects.get(id=id)
        
        nombre = request.POST['tematica']
        descripcion = request.POST['descripcion']
        materia_id = request.POST['materia']

        # Obtener la referencia de la materia en lugar de crear una nueva
        materia = get_object_or_404(Materia, id=materia_id)

        tematica.nombre = nombre
        tematica.descripcion = descripcion
        tematica.materia = materia
        tematica.save()
        return redirect('/profesores/tematicas/?message=La%20tematica%20ha%20sido%20actualizada%20correctamente')

def deleteTematica(request, id):
    tematica = get_object_or_404(Tematica, id=id)  # Usa get_object_or_404 para evitar errores si no existe
    tematica.delete()
    return redirect('/profesores/tematicas/?message=La%20tematica%20ha%20sido%20eliminada%20correctamente')
