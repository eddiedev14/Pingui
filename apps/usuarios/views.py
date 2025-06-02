from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import *

# Create your views here.

def signup(request):
    if request.method == 'POST':
        documento_papa = request.POST['father__document']
        nombre_papa = request.POST['father__name']
        email_papa = request.POST['father_email']
        password = request.POST['password']
        documento_pingui = request.POST['student__document']
        nombre_pingui = request.POST['student_name']

        responsable = Responsable.objects.create(
            documento=documento_papa,
            nombre = nombre_papa,
            correo = email_papa,
            contraseña = password
        )

        estudiante = Estudiante.objects.create(
            documento = documento_pingui,
            nombre = nombre_pingui,
            responsable = responsable
        )

        return redirect('/login_estudiantes/?message=El%20estudiante%20ha%20sido%20creado%20correctamente&icon=success')

def signin_estudiante(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')  
        password = request.POST.get('password', '')  

        # Verificamos que el responsable exista
        responsables = Responsable.objects.filter(correo=email, contraseña=password)

        if responsables.exists():
            responsable = responsables.first()

            # Obtener el primer estudiante asociado al responsable
            estudiante = Estudiante.objects.filter(responsable=responsable).first()

            request.session['Documento'] = estudiante.documento  # Guarda el documento del estudiante
            request.session['Nombre'] = estudiante.nombre  # Guarda el nombre del estudiante
            request.session['Email'] = responsable.correo
            request.session['Role'] = "Estudiante"
            
            return redirect('/estudiantes/dashboard/')    
        else:
            return redirect('/login_estudiantes/?message=El%20usuario%20no%20fue%20encontrado')


def signin_profesor(request):
    if request.method == 'POST':

        email = request.POST['email']
        password = request.POST['password']

        #Verificamos que el usuario exista
        docentes = Docente.objects.filter(correo=email, contraseña=password)

        if docentes.exists():
            docente = docentes.first()
            request.session['Nombre'] = docente.nombre
            request.session['Email'] = docente.correo
            request.session['Role'] = "Profesor"
            return redirect('/profesores/dashboard/')    
        else:
            return redirect('/login_profesores/?message=El%20usuario%20no%20fue%20encontrado')

def logout(request):
    try:
        del request.session['Nombre']
        del request.session['Email']
        del request.session['Role']
    except:
        return redirect("/")
    return redirect("/")

#*Profesores -> Estudiantes

def professor_students(request):
    listar = Estudiante.objects.all()
    return render(request, 'profesores/estudiantes/estudiantes.html', {'Estudiante':listar})

def deleteStudent(request, documento):
    estudiante = Estudiante.objects.get(documento=documento)
    responsable = estudiante.responsable  # Obtener el responsable asociado
    
    estudiante.delete()  # Eliminar el estudiante
    
    # Si el responsable no tiene más estudiantes, eliminarlo también
    if responsable and not responsable.estudiante_set.exists():
        responsable.delete()

    return redirect('/profesores/estudiantes/?message=El%20estudiante%20ha%20sido%20eliminado%20correctamente')

#*Profesores -> Responsables
def professor_responsables(request):
    listar = Responsable.objects.prefetch_related('estudiante_set').all()
    return render(request, 'profesores/responsables/responsables.html', {'Responsable':listar})