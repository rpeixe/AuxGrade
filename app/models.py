from django.db import models

from core.models import AbstractBaseModel


class Course(AbstractBaseModel):
    name = models.CharField('Nome da Disciplina', max_length=255, unique = True)
    semester = models.PositiveSmallIntegerField('Semestre', default = 1)
    hours = models.PositiveSmallIntegerField('Carga Horária', default = 72)
    required_courses = models.ManyToManyField('self', related_name = 'courses_that_require', symmetrical = False, blank = True)
    
    class Meta():
        ordering = ['name']

    def __str__(self):
        return self.name

class Degree(AbstractBaseModel):
    name = models.CharField('Nome do Curso', max_length = 255, unique = True)
    initials = models.CharField('Sigla', max_length = 3, unique = True)
    hours_total = models.SmallIntegerField('Carga Horária Total', default = 0)
    hours_core = models.SmallIntegerField('Carga Horária Fixas', default = 0)
    hours_elective = models.SmallIntegerField('Carga Horária Eletivas', default = 0)
    hours_ca = models.SmallIntegerField('Carga Horária Atividades Complementares', default = 0)
    hours_thesis = models.SmallIntegerField('Carga Horária TCC', default = 0)
    hours_internship = models.SmallIntegerField('Carga Horária Estagio', default = 0)
    courses = models.ManyToManyField(Course, related_name = 'degrees', blank = True, through = 'DegreeCourse')
    
    class Meta():
        ordering = ['name']

    def __str__(self):
        return self.name

class DegreeCourse(AbstractBaseModel):
    COURSE_TYPE_CHOICES = [
        ('CO', 'Fixa'),
        ('EL', 'Eletiva'),
        ('IN', 'Interdisciplinar'),
        ('OP', 'Optativa'),
    ]

    degree = models.ForeignKey(Degree, on_delete = models.CASCADE)
    course = models.ForeignKey(Course, on_delete = models.CASCADE)
    course_type = models.CharField('Tipo', max_length = 2, choices = COURSE_TYPE_CHOICES, default = 'CO')

    class Meta():
        ordering = ['degree__name', 'course__name']
        constraints = [
            models.UniqueConstraint(fields = ['degree', 'course'], name = 'unique_degreecourse_relation')
        ]

    def __str__(self):
        return f'{self.degree.name} - {self.course.name} ({self.course_type})'

class Section(AbstractBaseModel):
    course = models.ForeignKey(Course, on_delete = models.CASCADE)
    name = models.CharField('Nome da Turma', max_length = 255, unique = True)
    schedule = models.ManyToManyField('SectionTime', related_name = 'sections_scheduled')
    
    class Meta():
        ordering = ['name']

    def __str__(self):
        return self.name

class SectionTime(AbstractBaseModel):
    MONDAY = '0'
    TUESDAY = '1'
    WEDNESDAY = '2'
    THURSDAY = '3'
    FRIDAY = '4'
    SATURDAY = '5'
    SUNDAY = '6'

    DAY_OF_WEEK_CHOICES = [
        (MONDAY, 'Segunda'),
        (TUESDAY, 'Terça'),
        (WEDNESDAY, 'Quarta'),
        (THURSDAY, 'Quinta'),
        (FRIDAY, 'Sexta'),
        (SATURDAY, 'Sábado'),
        (SUNDAY, 'Domingo'),
    ]

    day = models.CharField('Dia', max_length = 1, choices = DAY_OF_WEEK_CHOICES, default = MONDAY)
    time = models.TimeField('Horário', default = '08:00')

    class Meta():
        ordering = ['day', 'time']
        constraints = [
            models.UniqueConstraint(fields = ['day', 'time'], name = 'unique_daytime_relation')
        ]

    def __str__(self):
        return self.get_day_display() + " " + str(self.time)

class CourseWeight(AbstractBaseModel):
    user = models.ForeignKey('account.User', related_name = 'course_weights', on_delete = models.CASCADE)
    course = models.ForeignKey(Course, related_name = 'user_weights', on_delete = models.CASCADE)
    weight = models.PositiveSmallIntegerField('Peso', default = 0)

class ComplimentaryHour(AbstractBaseModel):
    CITIZENSHIP_HOURS = '0'
    EXTENSION_HOURS = '1'
    ORIENTATION_HOURS = '2'
    ACADEMIC_HOURS = '3'

    COMPLIMENTARY_HOURS_CHOICE = [
        (CITIZENSHIP_HOURS, "Atividade de Formação Cidadã"),
        (EXTENSION_HOURS, "Atividade de Extensão"),
        (ORIENTATION_HOURS, "Atividade de Orientação Acadêmica"),
        (ACADEMIC_HOURS, "Atividades Acadêmica, Profissional e Artística"),
    ]

    user = models.ForeignKey('account.User', related_name = 'complimentary_hours', on_delete = models.CASCADE)
    name = models.CharField("Nome", max_length = 255)
    hours = models.PositiveSmallIntegerField("Horas", default = 0)
    group = models.CharField('Grupo', max_length = 1, choices = COMPLIMENTARY_HOURS_CHOICE, default = CITIZENSHIP_HOURS)

    class Meta():
        ordering = ['name']