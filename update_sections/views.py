from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.models import Section, Course

@login_required
def auto_update_sections(request):
    if request.user.is_staff:
        if request.method == 'POST':
            req = request.POST

            for course in req:
                course = Course.objects.get(name=req[course]['name'])
                for section in req[course]['sections']:
                    section_name = req[course]['sections'][section]['name']
                    section_schedule = req[course]['sections'][section]['Schedule']
                    new_section = Section(course = course, name = section_name, schedule = section_schedule)
                    new_section.save()



        return redirect('menu_principal')
    else:
        messages.error("Usuário não permitido.")
        return redirect('menu_principal')