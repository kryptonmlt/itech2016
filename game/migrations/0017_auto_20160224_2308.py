# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0016_auto_20160224_1518'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='log',
            name='city',
        ),
        migrations.AddField(
            model_name='log',
            name='account',
            field=models.ForeignKey(related_name='account_logs', default=None, blank=True, to='game.Account', null=True),
        ),
        migrations.AlterField(
            model_name='badge',
            name='account',
            field=models.ForeignKey(related_name='account_badges', to='game.Account'),
        ),
    ]
