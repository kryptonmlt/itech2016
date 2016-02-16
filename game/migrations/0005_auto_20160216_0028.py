# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_auto_20160216_0016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='last_attacked',
            field=models.DateTimeField(default=None, null=True, verbose_name=b'date attacked', blank=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='last_login_date',
            field=models.DateTimeField(default=None, null=True, verbose_name=b'date login', blank=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='last_received_gold',
            field=models.DateTimeField(default=None, null=True, verbose_name=b'date received gold', blank=True),
        ),
    ]
