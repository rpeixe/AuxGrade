# Generated by Django 4.1.1 on 2022-10-03 14:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_remove_degree_required_courses_and_more'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='degree',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='app.degree'),
        ),
        migrations.AddField(
            model_name='user',
            name='semester',
            field=models.SmallIntegerField(default=1, verbose_name='Semestre'),
        ),
        migrations.CreateModel(
            name='Take',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('section', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='app.section')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Finish',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('course', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='users_finished', to='app.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='finished_courses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='user',
            name='finish',
            field=models.ManyToManyField(through='account.Finish', to='app.course'),
        ),
        migrations.AddField(
            model_name='user',
            name='take',
            field=models.ManyToManyField(through='account.Take', to='app.section'),
        ),
    ]