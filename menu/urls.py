from django.urls import path
from . import views

urlpatterns =[
path('', views.menu_principal, name='menu_principal'),
path('menu_materias/', views.menu_materias, name='menu_materias'),
]
