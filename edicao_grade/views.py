import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from account.models import User
from app.models import Degree, Section, Course, CourseWeight, SectionTime
from django.contrib.auth.decorators import login_required


def get_user_schedule(user):
    schedule = []
    for section in user.sections.all():
        schedule.extend(section.schedule.all())
    return schedule

def get_user_courses(user):
    courses = []
    for section in user.sections.all():
        courses.append(section.course)
    return courses

@login_required
def grade_edit(request): 
        sections = Section.objects.all()
        user = request.user
        monday_courses = []
        tuesday_courses = []
        wednesday_courses = []
        thursday_courses = []
        friday_courses = []
        saturday_courses = []
        usections = user.sections.all()
        user_mon_sec = usections.filter(schedule__day = SectionTime.MONDAY)
        user_tue_sec = usections.filter(schedule__day = SectionTime.TUESDAY)
        user_wed_sec = usections.filter(schedule__day = SectionTime.WEDNESDAY)
        user_thu_sec = usections.filter(schedule__day = SectionTime.THURSDAY)
        user_fri_sec = usections.filter(schedule__day = SectionTime.FRIDAY)
        user_sat_sec = usections.filter(schedule__day = SectionTime.SATURDAY)
        user_courses = get_user_courses(user)
        user_schedule = get_user_schedule(user)

        for section in sections:
            if section not in usections:
                for section_time in section.schedule.all():
                    if section_time.day == SectionTime.MONDAY:
                        monday_courses.append(section)
                    if section_time.day == SectionTime.TUESDAY:
                        tuesday_courses.append(section)
                    if section_time.day == SectionTime.WEDNESDAY:
                        wednesday_courses.append(section)
                    if section_time.day == SectionTime.THURSDAY:
                        thursday_courses.append(section)
                    if section_time.day == SectionTime.FRIDAY:
                        friday_courses.append(section)
                    if section_time.day == SectionTime.SATURDAY:
                        saturday_courses.append(section)

        
        if request.method == 'POST':
            Choices = request.POST.getlist('courses')
            lista = []
            for Choice in Choices:
                if Choice != '------':
                    lista.append(Section.objects.get(name=Choice))
            
            for choice in lista:
                for choice2 in lista:
                    if choice != choice2:
                        if any(section_time in choice2.schedule.all() for section_time in choice.schedule.all()):
                            return HttpResponse('Conflito de horários entre duas matérias')
                if choice.schedule.all().count() > lista.count(choice):
                    return HttpResponse('Uma ou mais matérias selecionadas não foi selecionada em todos seus dias corretamente')
                user.sections.add(choice)
            
            return redirect('menu_principal')
        
        auto_grade(user, user_schedule,user_courses)

        context={
            'mon_courses':monday_courses,
            'tue_courses':tuesday_courses,
            'wed_courses':wednesday_courses,
            'thu_courses':thursday_courses,
            'fri_courses':friday_courses,
            'sat_courses':saturday_courses,
            'oito': datetime.time(8,0,0),
            'dez':datetime.time(10,0,0),
            'uma_meia':datetime.time(13,30,0),
            'tres_meia':datetime.time(15,30,0),
            'sete':datetime.time(19,0,0),
            'nove':datetime.time(21,0,0),
            'monday': SectionTime.MONDAY,
            'tuesday': SectionTime.TUESDAY,
            'wednesday': SectionTime.WEDNESDAY,
            'thursday': SectionTime.THURSDAY,
            'friday': SectionTime.FRIDAY,
            'saturday': SectionTime.SATURDAY,
            'user_mon_sec':user_mon_sec,
            'user_tue_sec':user_tue_sec,
            'user_wed_sec':user_wed_sec,
            'user_thu_sec':user_thu_sec,
            'user_fri_sec':user_fri_sec,
            'user_sat_sec':user_sat_sec,
	        'user_sections':user.sections.all(),
        }

        return render(request,'edicao_grade2.html',context)

def weight_courses(user):
    degree = user.degree
    degree_courses = degree.courses.all()

    for course in degree_courses:
        course_weight, created = CourseWeight.objects.get_or_create(user = user, course = course)
        course_weight.weight = 1
        course_weight.save()
    for course in degree_courses:
        if course.required_courses.all() != None:
            for prereq in course.required_courses.all():
                course_weight, created = CourseWeight.objects.get_or_create(user = user, course = prereq)
                course_weight.weight += 1
                course_weight.save()
    for course in degree_courses:
        if course.semester <= user.semester:
            course_weight = CourseWeight.objects.get(user = user, course = course)
            course_weight.weight += 1
            course_weight.save()


def auto_grade(user, user_schedule,user_courses):
    weight_courses(user)
    course_weights = CourseWeight.objects.filter(user = user).order_by('-weight')

    for course_weight in course_weights:
        sections = Section.objects.filter(course = course_weight.course)
        for section in sections:
            if (not any(section_time in user_schedule for section_time in section.schedule.all())) and (section.course not in user_courses):
                user.sections.add(section)
                user_schedule.extend(section.schedule)
                user_courses.append(section.course)