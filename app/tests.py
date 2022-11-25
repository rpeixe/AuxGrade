from datetime import timedelta
from time import sleep
from django.test import TestCase
from django.utils import timezone
from .models import *
from django.db import IntegrityError

# Create your tests here.
class TestAbstractBaseModel(TestCase):
    def test_uuid_uniqueness(self):
        object_1 = Course.objects.create(name = 'object 1')
        object_2 = Degree.objects.create(name = 'object 2', initials = 'o2')
        self.assertNotEqual(object_1.uuid, object_2.uuid)

    def test_created_at(self):
        object_3 = Course.objects.create(name = 'object 3')
        self.assertAlmostEqual(object_3.created_at, timezone.now(), delta = timedelta(seconds = 1))
        
    def test_updated_at(self):
        object_4 = Course.objects.create(name = 'banana')
        sleep(0.001)
        object_4.name = 'object 4'
        self.assertNotEqual(object_4.created_at, timezone.now())

class TestCourseModel(TestCase):
    def test_name_uniqueness(self):
        with self.assertRaises(IntegrityError) as e:
            Course.objects.create(name = 'object 1')
            Course.objects.create(name = 'object 1')
        self.assertTrue('UNIQUE constraint failed: app_course.name' in e.exception.args)