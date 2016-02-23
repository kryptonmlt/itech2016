# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0011_auto_20160223_2205'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='lands_owned',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='cost',
            name='lands_price',
            field=models.IntegerField(default=500),
        ),
        migrations.AlterField(
            model_name='log',
            name='date_occurred',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 23, 22, 23, 31, 899000, tzinfo=utc), verbose_name=b'date occurred'),
        ),
        migrations.AlterField(
            model_name='message',
            name='date_occurred',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 23, 22, 23, 31, 898000, tzinfo=utc), verbose_name=b'date occurred'),
        ),
    ]
