from django.contrib import admin

from .models import *

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'semester', 'hours')
    list_filter = ['semester', 'hours']
    search_fields = ['name']

class DegreeCourseInLine(admin.TabularInline):
    model = DegreeCourse
    extra = 0

class DegreeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'initials']}),
        ('Horas', {'fields': ['hours_total', 'hours_core', 'hours_elective', 'hours_ca', 'hours_thesis', 'hours_internship']}),
    ]
    list_display = ['name']
    search_fields = ['name']
    inlines = [DegreeCourseInLine]

admin.site.register(Course, CourseAdmin)
admin.site.register(Degree, DegreeAdmin)
admin.site.register(Section)
admin.site.register(SectionTime)
admin.site.register(ComplimentaryHour)