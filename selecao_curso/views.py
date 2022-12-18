from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from app.models import Degree
from django.contrib.auth.decorators import login_required


@login_required
def Degree_selection(request):
    try:
        return render(request,"selecao.html")
    except:
        return HttpResponse("Não foi possível carregar a página!")

@login_required
def BCT_selected(request):
    try:
        if request.method == 'GET':
            change_degree(request.user, 'BCT')
            return redirect('menu_principal')
    except:
        messages.error(request, 'Erro ao selecionar curso!')
        return redirect('degree_selection')

@login_required
def EComp_selected(request):
    try:
        if request.method == 'GET':
            change_degree(request.user, 'EC')
            return redirect('menu_principal')
    except:
        messages.error(request, 'Erro ao selecionar curso!')
        return redirect('degree_selection')

@login_required
def BCC_selected(request):
    try:
        if request.method == 'GET':
            change_degree(request.user, 'BCC')
            return redirect('menu_principal')
    except:
        messages.error(request, 'Erro ao selecionar curso!')
        return redirect('degree_selection')

def change_degree(user, initials):
    user.degree = Degree.objects.get(initials = initials)
    user.save()