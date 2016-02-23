# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0010_auto_20160223_2147'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='house_level',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='city',
            name='supply',
            field=models.IntegerField(default=50),
        ),
        migrations.AlterField(
            model_name='log',
            name='date_occurred',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 23, 22, 5, 57, 253000, tzinfo=utc), verbose_name=b'date occurred'),
        ),
        migrations.AlterField(
            model_name='message',
            name='date_occurred',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 23, 22, 5, 57, 252000, tzinfo=utc), verbose_name=b'date occurred'),
        ),
    ]
