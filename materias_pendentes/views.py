from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app.models import DegreeCourse

def get_missing_courses(user):
    "Retorna uma lista com as disciplinas fixas do curso do usuário que ele ainda não concluiu."
    missing_courses = []
    core_courses = DegreeCourse.objects.filter(course_type = "CO", degree = user.degree)
    for degree_course in core_courses:
        if degree_course.course not in user.finished_courses.all():
            missing_courses.append(degree_course.course)
    if user.degree.initials != 'BCT':
        bct_courses = DegreeCourse.objects.filter(course_type = "CO", degree__initials = 'BCT')
        for degree_course in bct_courses:
            if degree_course.course not in user.finished_courses.all() and degree_course.course not in missing_courses:
                missing_courses.append(degree_course.course)

    return missing_courses

@login_required
def materias_pendentes(request):
    user = request.user
    missing_courses = get_missing_courses(user)
    if (len(missing_courses)==0):
        missing_courses.append("Você já concluiu todas as matérias fixas. Parabéns :)")
    context = {
        'missing_courses': missing_courses,
    }

    return render(request,'materias_pendentes.html', context)