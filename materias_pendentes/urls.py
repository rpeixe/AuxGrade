from django.urls import path
from . import views

urlpatterns =[
    path('', views.materias_pendentes, name='materias_pendentes'),
]
