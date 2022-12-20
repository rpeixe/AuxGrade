from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.models import Section, Course, SectionTime


@login_required
def auto_update_sections(request):
    if not request.user.is_staff:
        messages.error(request, "Usuário não permitido.")
        return redirect('menu_principal')
    if request.method == 'POST':
        req = request.POST

        for element in req:
            course = Course.objects.filter(name=req[element]['name'])
            if not course.exists():
                raise Exception(req[element]['name'] + ' não existe')

            for section in req[element]['sections']:
                section_name = req[element]['sections'][section]['name']
                section_schedule = req[element]['sections'][section]['schedule']
                if verify_if_not_exist_section(course.first(), section_name):
                    new_section = Section(course=course.first(), name=section_name)
                    for schedules in section_schedule:
                        schedule = SectionTime.objects.filter(day=schedules[0], time=schedules[1]).first()
                        if not (SectionTime.objects.filter(day=schedules[0], time=schedules[1])).exists():
                            schedule = SectionTime(day=schedules[0], time=schedules[1])
                            schedule.save()
                        new_section.save()
                        new_section.schedule.add(schedule)
                    messages.info(request, req[element]['name'] + ' salvo com sucesso')

        return redirect('menu_principal')
    return redirect('menu_principal')


def verify_if_not_exist_section(course, section_name):
    section = Section.objects.filter(course=course, name=section_name)
    if section.exists():
        return 0
    return 1
