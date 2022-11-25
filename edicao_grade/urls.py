from django.urls import path
from . import views

urlpatterns =[
path('', views.grade_edit, name = 'editar_grade'),
#path('', views.auto_grade),
]
