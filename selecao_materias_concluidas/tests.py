from django.test import TestCase, Client
from django.urls import reverse
from .views import *
from account.models import User
from app.models import Course

# Create your tests here.
class TestViewsSelecaoMaterias(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username = "test")
        self.course_1 = Course.objects.create(name = "course 1")
        self.course_2 = Course.objects.create(name = "course 2")
        self.course_3 = Course.objects.create(name = "course 3")
        self.course_4 = Course.objects.create(name = "course 4")
        self.user.finished_courses.add(self.course_4)
        self.user.interested_courses.add(self.course_4)
        self.courses = ["course 1", "course 2"]

    def test_add_finished_courses(self):
        self.assertTrue(self.course_1 not in self.user.finished_courses.all())
        self.assertTrue(self.course_2 not in self.user.finished_courses.all())
        self.assertTrue(self.course_3 not in self.user.finished_courses.all())
        self.assertTrue(self.course_4 in self.user.finished_courses.all())
        add_finished_courses(self.user, self.courses)
        self.assertTrue(self.course_1 in self.user.finished_courses.all())
        self.assertTrue(self.course_2 in self.user.finished_courses.all())
        self.assertTrue(self.course_3 not in self.user.finished_courses.all())
        self.assertTrue(self.course_4 in self.user.finished_courses.all())

    def test_add_interested_courses(self):
        self.assertTrue(self.course_1 not in self.user.interested_courses.all())
        self.assertTrue(self.course_2 not in self.user.interested_courses.all())
        self.assertTrue(self.course_3 not in self.user.interested_courses.all())
        self.assertTrue(self.course_4 in self.user.interested_courses.all())
        add_interested_courses(self.user, self.courses)
        self.assertTrue(self.course_1 in self.user.interested_courses.all())
        self.assertTrue(self.course_2 in self.user.interested_courses.all())
        self.assertTrue(self.course_3 not in self.user.interested_courses.all())
        self.assertTrue(self.course_4 in self.user.interested_courses.all())
        
    def test_course_selection_response_not_logged_in(self):
        client = Client()
        response = client.get(reverse('course_selection'))
        self.assertEqual(response.status_code, 302)
        
    def test_course_selection_response_logged_in(self):
        client = Client()
        client.force_login(self.user)
        response = client.get(reverse('course_selection'))
        self.assertEqual(response.status_code, 200)

    def test_course_selection_response_content(self):
        client = Client()
        client.force_login(self.user)
        response = client.get(reverse('course_selection'))
        self.assertContains(response, 'course 1')

    def test_course_selection_post(self):
        client = Client()
        client.force_login(self.user)
        response = client.post(reverse('course_selection'), {'course_name': self.courses, 'save': True})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.course_1 in self.user.finished_courses.all())
        self.assertTrue(self.course_2 in self.user.finished_courses.all())
        self.assertTrue(self.course_3 not in self.user.finished_courses.all())
        self.assertTrue(self.course_4 in self.user.finished_courses.all())
        
    def test_interest_selection_response_not_logged_in(self):
        client = Client()
        response = client.get(reverse('interest_selection'))
        self.assertEqual(response.status_code, 302)

    def test_interested_selection_response_logged_in(self):
        client = Client()
        client.force_login(self.user)
        response = client.get(reverse('interest_selection'))
        self.assertEqual(response.status_code, 200)

    def test_interest_selection_response_content(self):
        client = Client()
        client.force_login(self.user)
        response = client.get(reverse('interest_selection'))
        self.assertContains(response, 'course 1')

    def test_interested_selection_post(self):
        client = Client()
        client.force_login(self.user)
        response = client.post(reverse('interest_selection'), {'course_name': self.courses, 'save': True})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.course_1 in self.user.interested_courses.all())
        self.assertTrue(self.course_2 in self.user.interested_courses.all())
        self.assertTrue(self.course_3 not in self.user.interested_courses.all())
        self.assertTrue(self.course_4 in self.user.interested_courses.all())