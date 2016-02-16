# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_auto_20160216_0028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='alliance',
            field=models.ForeignKey(default=None, blank=True, to='game.Alliance', null=True),
        ),
    ]
