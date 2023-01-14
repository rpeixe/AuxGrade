"""auxgrade URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path ,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('login.urls')),
    path ('', include('account.urls')),
    path('selecao/', include('selecao_curso.urls')),
    path('menu/', include('menu.urls')),
    path('perfil/', include('perfil.urls')),
    path('selecao_materias_concluidas/', include('selecao_materias_concluidas.urls')),
    path('editar_grade/',include('edicao_grade.urls')),
    path('materias_pendentes/',include('materias_pendentes.urls')),
    path('horas_complementares/', include('horas_complementares.urls')),
    path('atualizar_horarios/', include('upload_de_materias.urls'))
]
