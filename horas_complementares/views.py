from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app.models import ComplimentaryHour


# Create your views here.
@login_required
def complementary_hour(request):
    user = request.user

    if request.method == 'POST':
        activity_name = request.POST.get('autoSizingName')
        amount_of_hour = request.POST.get('autoSizingHours')
        classification_of_activity = request.POST.get('autoSizingEixo')
        if isnumber(amount_of_hour):
            add_complementary_hour(user, activity_name, amount_of_hour, classification_of_activity)

        activity_name_searched = request.POST.get('autoSizingNameSearched')
        amount_of_hour_searched = request.POST.get('autoSizingHoursSearched')
        classification_of_activity_searched = request.POST.get('autoSizingEixoSearched')

    all_registered_activities = ComplimentaryHour.objects.all()
    user_registered_activities = []
    for activity in all_registered_activities:
        activity.group = getNome(activity.group)
        if user == activity.user:
            user_registered_activities.append(activity)

    citizenship_hour = 0
    extension_hour = 0
    orientation_hour = 0
    academic_hour = 0
    for activity in user_registered_activities:
        if activity.group == "Atividades Acadêmica, Profissional e Artística":
            academic_hour = academic_hour + float(activity.hours)
        elif activity.group == "Atividade de Orientação Acadêmica":
            orientation_hour = orientation_hour + float(activity.hours)
        elif activity.group == "Atividade de Extensão":
            extension_hour = extension_hour + float(activity.hours)
        else:
            citizenship_hour = citizenship_hour + float(activity.hours)
    missing_hour = 420 - sum(citizenship_hour, extension_hour, orientation_hour, academic_hour)
    context = {
        'user': user,
        'citizenship_hours': citizenship_hour,
        'extension_hours': extension_hour,
        'orientation_hours': orientation_hour,
        'academic_hours': academic_hour,
        'missing_hours': missing_hour,
        'activities': user_registered_activities,
    }
    return render(request, 'horas_complementares.html', context)


def sum(parcela1, parcela2, parcela3, parcela4):
    return parcela1 + parcela2 + parcela3 + parcela4

def isnumber(number):
    try:
        float(number)
        return True
    except:
        return False

def getNome(classification_of_activity):
    if float(classification_of_activity) == float(3):
        return "Atividades Acadêmica, Profissional e Artística"
    elif float(classification_of_activity) == float(2):
        return "Atividade de Orientação Acadêmica"
    elif (classification_of_activity) == float(1):
        return "Atividade de Extensão"
    else:
        return "Atividade de Formação Cidadã"

def add_complementary_hour(user, activity_name, amount_of_hour, classification_of_activity):
    if isNew(user,activity_name,amount_of_hour,classification_of_activity):
        if float(classification_of_activity) == float(3):
            ComplimentaryHour.objects.create(user=user, name=activity_name, hours=amount_of_hour,
                                         group=ComplimentaryHour.ACADEMIC_HOURS)
        elif float(classification_of_activity) == float(2):
            ComplimentaryHour.objects.create(user=user, name=activity_name, hours=amount_of_hour,
                                             group=ComplimentaryHour.ORIENTATION_HOURS)
        elif float(classification_of_activity) == float(1):
            ComplimentaryHour.objects.create(user=user, name=activity_name, hours=amount_of_hour,
                                             group=ComplimentaryHour.EXTENSION_HOURS)
        else:
            ComplimentaryHour.objects.create(user=user, name=activity_name, hours=amount_of_hour,
                                             group=ComplimentaryHour.CITIZENSHIP_HOURS)

def isNew(user, activity_name, amount_of_hour, classification_of_acitivity):
    saved_complimentary_hours = ComplimentaryHour.objects.all()
    for saved_complimentary_hour in saved_complimentary_hours:
        equality_count = 0
        if saved_complimentary_hour.user == user:
            equality_count = equality_count + 1
        if saved_complimentary_hour.name == activity_name:
            equality_count = equality_count + 1
        if float(saved_complimentary_hour.hours) == float(amount_of_hour):
            equality_count = equality_count + 1
        if float(saved_complimentary_hour.group) == float(classification_of_acitivity):
            equality_count = equality_count + 1
        if equality_count == 4:
            return False
    return True
