from django.test import TestCase
from account.models import User
from app.models import Degree
from .views import *

# Create your tests here.
class TestViewsSelecaoCurso(TestCase):
    def test_change_degree(self):
        degree_1 = Degree.objects.create(name = 'degree 1', initials = 'd1')
        degree_2 = Degree.objects.create(name = 'degree 2', initials = 'd2')
        user = User.objects.create_user(username = 'test')
        user.degree = degree_1
        self.assertEqual(user.degree, degree_1)
        change_degree(user, 'd2')
        self.assertEqual(user.degree, degree_2)