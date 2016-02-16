# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_auto_20160215_2312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='alliance',
            field=models.ForeignKey(default=None, to='game.Alliance'),
        ),
        migrations.AlterField(
            model_name='account',
            name='last_attacked',
            field=models.DateTimeField(default=None, verbose_name=b'date attacked'),
        ),
        migrations.AlterField(
            model_name='account',
            name='last_login_date',
            field=models.DateTimeField(default=None, verbose_name=b'date login'),
        ),
        migrations.AlterField(
            model_name='account',
            name='last_received_gold',
            field=models.DateTimeField(default=None, verbose_name=b'date received gold'),
        ),
        migrations.AlterField(
            model_name='account',
            name='picture',
            field=models.ImageField(upload_to=b'media', blank=True),
        ),
    ]
