from django.shortcuts import render, redirect
from app.models import Section, Course, CourseWeight, SectionTime, DegreeCourse
from django.contrib.auth.decorators import login_required
from .forms import HorariosForm
from django.contrib import messages

#@login_required
def horarios_livres(request): 
        user = request.user

        if request.method == 'POST':
            Form = HorariosForm(request.POST)
            section_times = SectionTime.objects.all()
            i = 0

            if Form.is_valid():
                user.free_times.clear()
                for day in Form.cleaned_data:
                    section_time_selected = Form.cleaned_data[day]
                    if section_time_selected:
                        section_time = section_times[i]
                        user.free_times.add(section_time)
                    i += 1
                return redirect('/editar_grade/auto')
            for error in list(Form.errors.values()):
                messages.error(request, error)


        Form = HorariosForm()
        return render(request, 'index.html', {'Form': Form})
