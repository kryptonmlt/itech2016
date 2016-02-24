# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0012_auto_20160223_2223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='picture',
            field=models.ImageField(upload_to=b'portraits', blank=True),
        ),
        migrations.AlterField(
            model_name='log',
            name='date_occurred',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 24, 0, 26, 49, 183000, tzinfo=utc), verbose_name=b'date occurred'),
        ),
        migrations.AlterField(
            model_name='message',
            name='date_occurred',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 24, 0, 26, 49, 182000, tzinfo=utc), verbose_name=b'date occurred'),
        ),
    ]
