from django.shortcuts import render, redirect
from account.models import User
from django.contrib.auth.decorators import login_required
from .forms import SemesterForm
from django.contrib import messages


@login_required
def show_profile(request):
    user = User.objects.get(username=request.user)
    degree = user.degree
    semester = user.semester
    if request.method == 'POST':
        form = SemesterForm(request.POST)
        if form.is_valid():
            new_semester = form.cleaned_data['semester']
            user.semester = new_semester
            user.save()
            return redirect("/perfil/")
        for error in list(form.errors.values()):
            messages.error(request, error)
        
    form = SemesterForm(initial={'semester':semester})
    
    if user.degree_end != 0:
        remaining_semesters = user.degree_end
    else:
        remaining_semesters = ''

    context = {
        'user':user,
        'degree':degree,
        'remaining_semesters':remaining_semesters,
        'form':form,
    }
    return render(request, "perfil.html", context)

@login_required
def calc_remaining_time(request):
    user = User.objects.get(username=request.user)
    if user.degree != None:
        degree = user.degree
        core_hours = degree.hours_core
        finished_courses = user.finished_courses.all()
        if finished_courses != None:
            for course in finished_courses:
                core_hours -= course.hours
        
        if degree.initials == 'BCT':
            remaining_semesters = core_hours/292
        if degree.initials == 'BCC':
            remaining_semesters = core_hours/165
        if degree.initials == 'EC':
            remaining_semesters = core_hours/342
    
    if remaining_semesters > 0 and remaining_semesters < 1:
        remaining_semesters = 1
    else:
        remaining_semesters = int(remaining_semesters)

        user.degree_end = remaining_semesters
        user.save()
    return redirect('/perfil')