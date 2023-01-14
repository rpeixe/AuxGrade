from django.db import models

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator

from core.models import AbstractBaseModel


class User(PermissionsMixin, AbstractBaseUser, AbstractBaseModel):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField('Username', max_length=255, unique=True, validators=[username_validator])
    email = models.EmailField('Email address', unique=True)
    is_active = models.BooleanField('Active', default=True)
    degree = models.ForeignKey('app.Degree', on_delete = models.PROTECT, null = True, blank = True)
    sections = models.ManyToManyField('app.Section', related_name = 'students', blank = True)
    finished_courses = models.ManyToManyField('app.Course', related_name = 'users_that_finished', blank = True)
    interested_courses = models.ManyToManyField('app.Course', related_name = 'users_interested', blank = True)
    free_times = models.ManyToManyField('app.SectionTime', related_name = 'users_free', blank = True)
    semester = models.SmallIntegerField('Semestre', default = 1)
    weights = models.ManyToManyField('app.Course', related_name = 'user_weight', through = 'app.CourseWeight')
    degree_end = models.IntegerField('Expected Hours', default = 0)
    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can log into this admin site.'
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    @property
    def is_django_user(self):
        return self.has_usable_password()
