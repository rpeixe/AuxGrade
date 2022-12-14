from django.urls import path
from . import views

urlpatterns =[
path('', views.grade_edit, name = 'editar_grade'),
path('auto', views.auto_grade, name = 'auto_grade'),
]
