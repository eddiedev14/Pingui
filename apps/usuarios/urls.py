"""
URL configuration for pingui project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from . import views
from django.urls import path

urlpatterns = [
    #* Login
    path('estudiante/signup/', views.signup),
    path('estudiante/signin/', views.signin_estudiante),
    path('profesor/signin/', views.signin_profesor),
    path('logout/', views.logout),

    #*Profesores -> Estudiantes
    path('profesores/estudiantes/', views.professor_students),
    path('profesores/estudiantes/deleteStudent/<documento>/', views.deleteStudent),

    #*Profesores -> Responsables
    path('profesores/responsables/', views.professor_responsables),
]
