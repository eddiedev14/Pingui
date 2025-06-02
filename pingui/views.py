from django.shortcuts import render

# Create your views here.
def landing_page(request):
    return render(request, 'home/index.html')

def login_estudiantes(request):
    return render(request, 'home/loginEstudiantes.html')

def login_profesores(request):
    return render(request, 'home/loginProfesores.html')

def signup(request):
    return render(request, 'home/signup.html')

#* Administador

def admin_profesores(request):
    return render(request, 'profesores/dashboardProfesores.html')

#* Administador

def admin_estudiantes(request):
    return render(request, 'estudiantes/dashboardEstudiantes.html')