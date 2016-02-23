# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0009_auto_20160223_2124'),
    ]

    operations = [
        migrations.CreateModel(
            name='CityGraphic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.IntegerField(default=0)),
                ('picture', models.ImageField(upload_to=b'media', blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='log',
            name='date_occurred',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 23, 21, 47, 7, 213000, tzinfo=utc), verbose_name=b'date occurred'),
        ),
        migrations.AlterField(
            model_name='message',
            name='date_occurred',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 23, 21, 47, 7, 212000, tzinfo=utc), verbose_name=b'date occurred'),
        ),
    ]
