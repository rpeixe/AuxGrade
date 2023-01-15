from django.urls import path
from . import views

urlpatterns =[
path('', views.horarios_livres, name = 'horarios_livres'),
]
