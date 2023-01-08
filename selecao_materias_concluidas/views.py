from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from app.models import Course
from django.contrib.auth.decorators import login_required


def add_finished_courses(user, course_names):
    "Marca disciplinas como finalizadas para um usuário a partir de uma lista de nomes."
    for course_name in course_names:
        user.finished_courses.add(Course.objects.get(name = course_name))

def add_interested_courses(user, course_names):
    "Marca disciplinas como de interesse para um usuário a partir de uma lista de nomes."
    for course_name in course_names:
        user.interested_courses.add(Course.objects.get(name = course_name))

@login_required
def course_selection(request):
    user = request.user

    if request.method == 'POST':
        if 'save' in request.POST:
            finished_courses = request.POST.getlist('course_name')
            add_finished_courses(user, finished_courses)
            return redirect('menu_principal')
        elif 'searched' in request.POST:
            filtered_course_name = request.POST.get('filtered')
            context={
                'courses':Course.objects.filter(name__icontains=filtered_course_name)
            }
            return render(request, 'selecao_materias.html', context)
        
    else:
        context={
        'courses':Course.objects.all(),
    }

    return render(request,'selecao_materias.html', context)

@login_required
def interest_selection(request):
    user = request.user

    if request.method == 'POST':
        if 'save' in request.POST:
            finished_courses = request.POST.getlist('course_name')
            add_finished_courses(user, finished_courses)
            return redirect('menu_principal')
        elif 'searched' in request.POST:
            filtered_course_name = request.POST.get('filtered')
            context = {
                'courses': Course.objects.filter(name__icontains=filtered_course_name)
            }
            return render(request, 'selecao_materias.html', context)
        
    else:
        context={
        'courses':Course.objects.all(),
    }

    return render(request,'materias_de_interesse.html', context)