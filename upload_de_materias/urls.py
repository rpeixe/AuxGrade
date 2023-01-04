from django.urls import path
from . import views

urlpatterns =[
path('', views.upload_file, name='upload_de_materias'),
path('upload_finalizado', views.upload_finalizado, name='upload_finalizado'),
]
