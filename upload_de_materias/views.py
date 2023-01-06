from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from app.models import Section, Course, SectionTime
from django.http import HttpResponseRedirect
from .forms import UploadFileForm
import pandas as pd
import time
import os
from auxgrade.settings import BASE_DIR

# Imaginary function to handle an uploaded file.
@user_passes_test(lambda u: u.is_superuser)
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('upload_finalizado')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def handle_uploaded_file(f):
    with open('file/upload.xlsx', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

@user_passes_test(lambda u: u.is_superuser)
def upload_finalizado(request):
   return render(request,"upload_finalizado.html")

@user_passes_test(lambda u: u.is_superuser)
def auto_update_sections(request):
    if not request.user.is_staff:
        messages.error(request, "Usuário não permitido.")
        return redirect('menu_principal')

    df = pd.read_excel(os.path.join(BASE_DIR, 'file/upload.xlsx'))
    req = get_sections(df)

    Section.objects.all().delete()

    for element in req:
        course = Course.objects.filter(name__iexact=req[element]['name'])
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
            course = str(df.iloc[i][j]).replace('(reof)', '').replace('(Reof)', '').replace('(REOF)', '').replace('(turma adicional)', '').strip()
            section_name = str(df.iloc[i+1][j]).strip()
            section_code = section_name.split("-")[0].strip()

            k = j
            while (str(df.iloc[0][k]) == "nan"):
                k -= 1
            section_day = get_day(str(df.iloc[0][k]).split()[0])
            section_time = time.strftime("%H:%M", time.strptime(str(df.iloc[i][1]).split("-")[0].strip(), "%Hh%M"))

            if course != "nan" and course != "" and not course.startswith("TCC") and not course.startswith("ECOS") and not course.startswith("TG") and course != "Estágio":
                if course not in sections:
                    sections[course] = {
                        "name": course,
                        "sections": {},
                    }
                if section_code not in sections[course]["sections"]:
                    sections[course]["sections"][section_code] = {
                        "name": course + " - " + section_name,
                        "schedule": [],
                    }
                sections[course]["sections"][section_code]["schedule"].append((section_day, section_time))

    return sections

def get_day(str):
    if str == 'Segunda':
        return '0'
    if str == 'Terça':
        return '1'
    if str == 'Quarta':
        return '2'
    if str == 'Quinta':
        return '3'
    if str == 'Sexta':
        return '4'
    if str == 'Sábado':
        return '5'
    if str == 'Domingo':
        return '6'
    raise Exception('Erro no dia "' + str + '"')