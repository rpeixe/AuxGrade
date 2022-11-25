from django.urls import path
from . import views

urlpatterns =[
path('', views.Degree_selection),
path('BCT_selected/', views.BCT_selected),
path('BCC_selected/',views.BCC_selected),
path('EComp_selected/',views.EComp_selected),
]
