# Generated by Django 4.1.1 on 2022-10-26 01:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_degree_initials'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ['name']},
        ),
    ]
