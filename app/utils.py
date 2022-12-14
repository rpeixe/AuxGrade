from .models import SectionTime

def create_section_times():
    SectionTime.objects.all().delete()
    days = [SectionTime.MONDAY, SectionTime.TUESDAY, SectionTime.WEDNESDAY, SectionTime.THURSDAY, SectionTime.FRIDAY, SectionTime.SATURDAY]
    times = ['08:00', '10:00', '13:30', '15:30', '19:00', '21:00']
    for day in days:
        for time in times:
            SectionTime.objects.create(day = day, time = time)