from django.urls import path
from . import views

urlpatterns =[
path('atualizar/', views.auto_update_sections, name = 'update_sections'),
path('upload/', views.upload_file, name='upload_de_materias'),
path('upload/upload_finalizado/', views.upload_finalizado, name='upload_finalizado'),
]
