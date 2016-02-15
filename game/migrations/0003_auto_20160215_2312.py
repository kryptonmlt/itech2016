# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('game', '0002_auto_20160215_2246'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='email',
        ),
        migrations.RemoveField(
            model_name='account',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='account',
            name='password',
        ),
        migrations.RemoveField(
            model_name='account',
            name='surname',
        ),
        migrations.RemoveField(
            model_name='account',
            name='username',
        ),
        migrations.AddField(
            model_name='account',
            name='user',
            field=models.OneToOneField(default=None, to=settings.AUTH_USER_MODEL),
        ),
    ]
