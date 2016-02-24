# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0014_auto_20160224_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='last_received_gold',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date received gold'),
        ),
        migrations.AlterField(
            model_name='alliancerequest',
            name='date_occurred',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date occurred'),
        ),
        migrations.AlterField(
            model_name='log',
            name='date_occurred',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date occurred'),
        ),
        migrations.AlterField(
            model_name='message',
            name='date_occurred',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date occurred'),
        ),
    ]
