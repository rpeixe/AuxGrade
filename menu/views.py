from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def menu_principal(request):
    return render(request,"menu_principal.html")

@login_required
def menu_materias(request):
    return render(request,"menu_materias.html")