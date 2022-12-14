# Generated by Django 4.1.1 on 2022-10-09 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_remove_degreerequirement_course_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='is_interdisciplinary',
            field=models.BooleanField(default=False, verbose_name='Interdisciplinar'),
        ),
        migrations.AlterField(
            model_name='degree',
            name='core_courses',
            field=models.ManyToManyField(blank=True, related_name='core_in_degrees', to='app.course'),
        ),
        migrations.AlterField(
            model_name='degree',
            name='elective_courses',
            field=models.ManyToManyField(blank=True, related_name='elective_in_degrees', to='app.course'),
        ),
    ]