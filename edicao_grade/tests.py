from django.test import TestCase, Client
from django.urls import reverse
from account.models import User
from app.models import Course, Section, SectionTime, Degree
from .views import *

# Create your tests here.
class TestViewsEdicaoGrade(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username = 'user')
        self.degree = Degree.objects.create(name = 'degree', initials = 'd')
        self.user.degree = self.degree
        self.user.save()
        self.course_1 = Course.objects.create(name = 'course 1')
        self.course_2 = Course.objects.create(name = 'course 2')
        self.course_3 = Course.objects.create(name = 'course 3')
        monday_0800 = SectionTime.objects.create(day = SectionTime.MONDAY, time = '08:00')
        monday_1000 = SectionTime.objects.create(day = SectionTime.MONDAY, time = '10:00')
        tuesday_0800 = SectionTime.objects.create(day = SectionTime.TUESDAY, time = '08:00')
        wednesday_0800 = SectionTime.objects.create(day = SectionTime.WEDNESDAY, time = '08:00')
        wednesday_1000 = SectionTime.objects.create(day = SectionTime.WEDNESDAY, time = '10:00')
        thursday_0800 = SectionTime.objects.create(day = SectionTime.THURSDAY, time = '08:00')
        friday_0800 = SectionTime.objects.create(day = SectionTime.FRIDAY, time = '08:00')
        self.section_1 = Section.objects.create(name = 'section 1', course = self.course_1)
        self.section_1.schedule.add(monday_0800)
        self.section_1.schedule.add(wednesday_0800)
        self.section_2 = Section.objects.create(name = 'section 2', course = self.course_2)
        self.section_2.schedule.add(tuesday_0800)
        self.section_2.schedule.add(thursday_0800)
        self.section_3 = Section.objects.create(name = 'section 3', course = self.course_2)
        self.section_3.schedule.add(monday_1000)
        self.section_3.schedule.add(wednesday_1000)
        self.section_4 = Section.objects.create(name = 'section 4', course = self.course_2)
        self.section_4.schedule.add(monday_0800)
        self.section_4.schedule.add(tuesday_0800)
        self.section_5 = Section.objects.create(name = 'section 5', course = self.course_1)
        self.section_5.schedule.add(monday_1000)
        self.section_5.schedule.add(wednesday_1000)
        self.client = Client()
        self.client.force_login(self.user)
        
    def test_response_logged_in(self):
        response = self.client.get(reverse('editar_grade'))
        self.assertEqual(response.status_code, 200)
        
    def test_response_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('editar_grade'))
        self.assertEqual(response.status_code, 302)

    def test_response_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('editar_grade'))
        self.assertEqual(response.status_code, 302)
        
    def test_add_section(self):
        response = self.client.post(reverse('editar_grade'), {'courses': ['section 1', 'section 1']})
        self.assertTrue(self.section_1 in self.user.sections.all())
        
    def test_add_sections_same_time(self):
        response = self.client.post(reverse('editar_grade'), {'courses': ['section 1', 'section 1', 'section 2', 'section 2']})
        self.assertTrue(self.section_1 in self.user.sections.all() and self.section_2 in self.user.sections.all())
        
    def test_add_sections_same_day(self):
        response = self.client.post(reverse('editar_grade'), {'courses': ['section 1', 'section 1', 'section 3', 'section 3']})
        self.assertTrue(self.section_1 in self.user.sections.all() and self.section_3 in self.user.sections.all())

    def test_add_sections_same_time_same_day(self):
        response = self.client.post(reverse('editar_grade'), {'courses': ['section 1', 'section 1', 'section 4', 'section 4']})
        self.assertTrue(self.section_1 not in self.user.sections.all() and self.section_3 not in self.user.sections.all())

    def test_add_sections_same_course(self):
        response = self.client.post(reverse('editar_grade'), {'courses': ['section 1', 'section 1', 'section 5', 'section 5']})
        self.assertTrue(self.section_1 not in self.user.sections.all() or self.section_5 not in self.user.sections.all())
        
    def test_add_sections_same_course_separately(self):
        response = self.client.post(reverse('editar_grade'), {'courses': ['section 1', 'section 1']})
        response = self.client.post(reverse('editar_grade'), {'courses': ['section 5', 'section 5']})
        self.assertTrue(self.section_1 not in self.user.sections.all() or self.section_5 not in self.user.sections.all())