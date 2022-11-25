from django.urls import path
from . import views

urlpatterns =[
    path('', views.course_selection, name='course_selection'),
    path('interesse/', views.interest_selection, name='interest_selection'),
]
