from django.urls import path
from . import views

urlpatterns =[
path('', views.show_profile),
path('calcular', views.calc_remaining_time),
]
