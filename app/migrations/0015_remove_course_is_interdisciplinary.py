# Generated by Django 4.1.1 on 2022-10-19 11:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_remove_degree_core_courses_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='is_interdisciplinary',
        ),
    ]