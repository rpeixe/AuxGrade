from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.models import Section, Course, SectionTime
import pandas as pd
import time

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


def get_sections(df):
    sections = {}

    for i in range(2, df.shape[0]):
        for j in range(2, df.shape[1]):
            if df.iloc[i][1] == "Docente" or str(df.iloc[i][1]) == "nan":
                break
            course = str(df.iloc[i][j])
            section_name = str(df.iloc[i+1][j])
            section_code = section_name.split("-")[0].strip()

            k = j
            while (str(df.iloc[0][k]) == "nan"):
                k -= 1
            section_day = df.iloc[0][k]
            section_time = time.strftime("%H:%M", time.strptime(str(df.iloc[i][1]).split()[0].split("-")[0], "%Hh%M"))

            if str(course) != "nan":
                if course not in sections:
                    sections[course] = {
                        "name": course,
                        "sections": {},
                    }
                if section_code not in sections[course]["sections"]:
                    sections[course]["sections"][section_code] = {
                        "name": section_name,
                        "schedule": [],
                    }
                sections[course]["sections"][section_code]["schedule"].append((section_day, section_time))

    return sections