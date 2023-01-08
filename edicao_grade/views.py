from django.http import HttpResponse
from django.shortcuts import redirect, render
from app.models import Section, Course, CourseWeight, SectionTime, DegreeCourse
from django.contrib.auth.decorators import login_required
from .forms import AgendaForm


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


        for section in sections:
            if section not in usections and verify_requirements(user, section.course):
                for section_time in section.schedule.all():
                    if section_time.day == SectionTime.MONDAY and section not in monday_courses:
                        monday_courses.append(section)
                    if section_time.day == SectionTime.TUESDAY and section not in tuesday_courses:
                        tuesday_courses.append(section)
                    if section_time.day == SectionTime.WEDNESDAY and section not in wednesday_courses:
                        wednesday_courses.append(section)
                    if section_time.day == SectionTime.THURSDAY and section not in thursday_courses:
                        thursday_courses.append(section)
                    if section_time.day == SectionTime.FRIDAY and section not in friday_courses:
                        friday_courses.append(section)
                    if section_time.day == SectionTime.SATURDAY and section not in saturday_courses:
                        saturday_courses.append(section)

        if request.method == 'POST':
            req = request.POST
            days = []
            user_selected_course = []
            lista = []
           
            for day in req:
                if(day != 'csrfmiddlewaretoken'):
                    days.append(day)
            
            for day in days:
                choices = request.POST.getlist(day)
                for choice in choices:
                    if(choice != '1' and choice != '0'):
                        lista.append(choice)
            
            chosen_section_list =[]

            user_remove_section(user, usections, req)

            for choice in lista:   
                    chosen_section_list.append(Section.objects.get(name=choice))
            for chosen_section in chosen_section_list:
                if selected_section_is_invalid(chosen_section, chosen_section_list):
                    return HttpResponse('Conflito de horários entre matérias')
                if remove_section_and_verify_time_conflict(user, chosen_section):
                    return HttpResponse('Turmas de uma mesma matéria ja foi selecionada')
                user.sections.add(chosen_section)
                user_selected_course.append(chosen_section)
          
            return redirect('editar_grade')
        monForm = AgendaForm(courses = monday_courses,day="0",user_sec = user_mon_sec)
        tueForm = AgendaForm(courses = tuesday_courses,day="1",user_sec = user_tue_sec)
        wedForm = AgendaForm(courses = wednesday_courses,day="2",user_sec = user_wed_sec)
        thuForm = AgendaForm(courses = thursday_courses,day="3",user_sec = user_thu_sec)
        friForm = AgendaForm(courses = friday_courses,day="4",user_sec = user_fri_sec)
        satForm = AgendaForm(courses = saturday_courses,day="6",user_sec = user_sat_sec)

        return render(request, 'edicao_grade.html', {
        'monForm': monForm,
        'tueForm': tueForm,
        'wedForm': wedForm,
        'thuForm': thuForm,
        'friForm': friForm,
        'satForm': satForm,
    })

def user_remove_section(user, userSections, dictionary):
    days = []
    sections_to_remove = []

    for day in dictionary: #Pega os horarios e dias corretamente
        if(day != 'csrfmiddlewaretoken'):
            days.append(day)

    for index, day in enumerate(days):
        sections = dictionary.getlist(day) #Cria uma lista com os horarios e dias
        for indexDay, weekDay in enumerate(sections):
            if weekDay == '1': #para dias com valor 1
                for section in userSections: #testa com todos as sections do usuario
                    sectionSchedule = section.schedule.all()
                    for sectionTime in sectionSchedule:
                        day_correct = day+':00'
                        if day_correct == '8:00:00':
                            day_correct = '0'+day_correct #Para transformar a string de modo que fique igual as seçoes do usuario
                        if indexDay == int(sectionTime.day) and day_correct == str(sectionTime.time): #Se uma seçao apresentar o mesmo dia e horario
                            sections_to_remove.append(section) #sections para serem removidas

    for section in sections_to_remove:
        user.sections.remove(section)

def remove_section_and_verify_time_conflict(user, section):
    course_that_should_be_removed = []
    for schedule in section.schedule.all():
        user_filtered_sections = user.sections.filter(schedule=schedule)
        if user_filtered_sections != None:
            for sec in user.sections.filter(schedule=schedule):
                course_that_should_be_removed.append(sec.course)
        user_courses = get_user_courses(user)
        if section.course in user_courses and section.course not in course_that_should_be_removed:
            return 1
        for section in user_filtered_sections:
            user.sections.remove(section)

def selected_section_is_invalid(chosen_section, section_list):
    for chosen_section2 in section_list:
        if chosen_section != chosen_section2:
            if any(section_time in chosen_section2.schedule.all() for section_time in chosen_section.schedule.all()):
                return 1

def weight_courses(user):
    CourseWeight.objects.filter(user=user).delete()
    user.sections.clear()
    in_courses_completed = get_in_courses_completed(user)
    degree = user.degree

    for course in Course.objects.all():
        if verify_requirements(user, course):
            course_weight = CourseWeight.objects.create(user=user, course=course)

    degree_courses = degree.courses.all()
    for course_weight in user.course_weights.all():
        weight = 10 - course_weight.course.semester
        if course_weight.course.semester == user.semester:
            weight += 16
        user_degree_course = DegreeCourse.objects.filter(degree = user.degree, course = course_weight.course).first()
        if user_degree_course and user_degree_course.course_type == 'CO':
            weight += 256
        if any(required_course in course_weight.course.courses_that_require.all() for required_course in DegreeCourse.objects.filter(degree = degree, course_type = 'CO')):
            weight += 128
        bct_degree_course = DegreeCourse.objects.filter(degree__initials = 'BCT', course = course_weight.course).first()
        if bct_degree_course and bct_degree_course.course_type == 'CO':
            weight += 256
        if bct_degree_course and bct_degree_course.course_type == 'IN' and in_courses_completed < 4:
            weight += 64
        if course_weight.course in user.interested_courses.all() or any(course_weight.course in interested_course.required_courses.all() for interested_course in user.interested_courses.all()):
            weight += 32
        course_weight.weight = weight
        course_weight.save()

def auto_grade(request):
    user = request.user
    weight_courses(user)
    user_courses = get_user_courses(user)
    user_schedule = get_user_schedule(user)
    course_weights = CourseWeight.objects.filter(user = user).order_by('-weight')
    for course_weight in course_weights:
        sections = Section.objects.filter(course = course_weight.course)
        for section in sections:
            if (not any(section_time in user_schedule for section_time in section.schedule.all())) \
                    and (section.course not in user_courses):
                user.sections.add(section)
                user_schedule.extend(section.schedule.all())
                user_courses.append(section.course)
    return redirect("editar_grade")

def verify_requirements(user, course):
    finished_courses = user.finished_courses.all()
    return not any(required_course not in finished_courses for required_course in course.required_courses.all()) and course not in finished_courses

def get_in_courses_completed(user):
    finished_courses = user.finished_courses.all()
    num = 0
    for course in finished_courses:
        degree_course = DegreeCourse.objects.filter(degree__initials = 'BCT', course = course).first()
        if degree_course and degree_course.course_type == 'IN':
            num += 1
    return num

def get_el_hours(user):
    finished_courses = user.finished_courses.all()
    degree = user.degree
    num = 0
    for course in finished_courses:
        degree_course = DegreeCourse.objects.filter(degree = degree, course = course).first
        if degree_course and degree_course.course_type != 'CO':
                num += course.hours
        else:
            num += course.hours
    return num
