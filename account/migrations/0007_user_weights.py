# Generated by Django 4.1.1 on 2022-11-22 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_remove_course_weight_courseweight'),
        ('account', '0006_user_free_times_user_interested_courses'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='weights',
            field=models.ManyToManyField(related_name='user_weight', through='app.CourseWeight', to='app.course'),
        ),
    ]
