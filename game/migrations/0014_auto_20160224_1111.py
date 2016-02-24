# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0013_auto_20160224_0026'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='supply',
        ),
        migrations.AlterField(
            model_name='account',
            name='last_received_gold',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 24, 11, 11, 19, 233000, tzinfo=utc), verbose_name=b'date received gold'),
        ),
        migrations.AlterField(
            model_name='alliancerequest',
            name='date_occurred',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 24, 11, 11, 19, 236000, tzinfo=utc), verbose_name=b'date occurred'),
        ),
        migrations.AlterField(
            model_name='city',
            name='gold',
            field=models.IntegerField(default=1000),
        ),
        migrations.AlterField(
            model_name='log',
            name='date_occurred',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 24, 11, 11, 19, 238000, tzinfo=utc), verbose_name=b'date occurred'),
        ),
        migrations.AlterField(
            model_name='message',
            name='date_occurred',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 24, 11, 11, 19, 237000, tzinfo=utc), verbose_name=b'date occurred'),
        ),
    ]
