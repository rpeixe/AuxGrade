# Generated by Django 4.1.1 on 2022-12-18 23:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_user_course_end'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='course_end',
            new_name='degree_end',
        ),
    ]
