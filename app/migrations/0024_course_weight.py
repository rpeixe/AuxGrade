# Generated by Django 4.1.1 on 2022-11-20 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_alter_degree_initials'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='weight',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='weight'),
        ),
    ]