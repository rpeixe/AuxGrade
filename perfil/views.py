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
    context = {
        'user':user,
        'degree':degree,
        'form':form,
    }
    return render(request, "perfil.html", context)
