from django.urls import path
from . import views

urlpatterns =[
path('', views.auto_update_sections, name = 'update_sections'),
]
