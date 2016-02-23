# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0008_auto_20160221_1453'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alliancerequest',
            name='alliance_owner',
        ),
        migrations.AddField(
            model_name='alliancerequest',
            name='alliance',
            field=models.ForeignKey(related_name='alliance_owner_request', default=None, blank=True, to='game.Alliance', null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='alliance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='game.Alliance', null=True),
        ),
        migrations.AlterField(
            model_name='log',
            name='date_occurred',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 23, 21, 24, 35, 393000, tzinfo=utc), verbose_name=b'date occurred'),
        ),
        migrations.AlterField(
            model_name='message',
            name='date_occurred',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 23, 21, 24, 35, 392000, tzinfo=utc), verbose_name=b'date occurred'),
        ),
    ]
