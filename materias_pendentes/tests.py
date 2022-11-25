from django.test import TestCase, Client
from django.urls import reverse
from account.models import User
from app.models import Course, Degree, DegreeCourse
from .views import get_missing_courses


class TestViewsMateriasPendentes(TestCase):
    def setUp(self):
        self.course_1 = Course.objects.create(name = 'course 1')
        self.course_2 = Course.objects.create(name = 'course 2')
        self.course_3 = Course.objects.create(name = 'course 3')
        self.degree = Degree.objects.create(name = 'degree', initials = 'd')
        self.degree.courses.add(self.course_1, self.course_2, self.course_3)
        dc1 = DegreeCourse.objects.get(degree = self.degree, course = self.course_1)
        dc1.course_type = 'CO'
        dc1.save()
        dc2 = DegreeCourse.objects.get(degree = self.degree, course = self.course_2)
        dc2.course_type = 'CO'
        dc2.save()
        dc3 = DegreeCourse.objects.get(degree = self.degree, course = self.course_3)
        dc3.course_type = 'EL'
        dc3.save()
        self.user = User.objects.create_user(username = 'name', password = 'password', email = 'email@test.com')
        self.user.degree = self.degree
        self.user.save()
        self.user.finished_courses.add(self.course_2)
        
    def test_missing_course(self):
        missing_courses = get_missing_courses(self.user)
        self.assertTrue(self.course_1 in missing_courses)
        
    def test_completed_course(self):
        missing_courses = get_missing_courses(self.user)
        self.assertTrue(self.course_2 not in missing_courses)

    def test_not_core_course(self):
        missing_courses = get_missing_courses(self.user)
        self.assertTrue(self.course_3 not in missing_courses)
        
    def test_response_not_logged_in(self):
        client = Client()
        response = client.get(reverse('materias_pendentes'))
        self.assertEqual(response.status_code, 302)

    def test_response_logged_in(self):
        client = Client()
        client.force_login(self.user)
        response = client.get(reverse('materias_pendentes'))
        self.assertEqual(response.status_code, 200)

    def test_response_content(self):
        client = Client()
        client.force_login(self.user)
        response = client.get(reverse('materias_pendentes'))
        self.assertContains(response, 'course 1')