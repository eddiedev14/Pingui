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
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing_page, name='landing_page'),
    path('login_estudiantes/', views.login_estudiantes, name='login_estudiantes'),
    path('login_profesores/', views.login_profesores, name='login_profesores'),
    path('registro/', views.signup, name='signup'),

    #*Administrador
    path('profesores/dashboard/', views.admin_profesores, name='admin_dashboard'),
    path('estudiantes/dashboard/', views.admin_estudiantes, name='admin_dashboard'),

    path('', include('apps.usuarios.urls')),
    path('', include('apps.cursos.urls')),
    path('', include('apps.evaluaciones.urls')),
]
