# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0026_auto_20160225_2232'),
    ]

    operations = [
        migrations.AddField(
            model_name='cost',
            name='gold_income',
            field=models.IntegerField(default=100),
        ),
        migrations.AddField(
            model_name='cost',
            name='lumber_income',
            field=models.IntegerField(default=25),
        ),
        migrations.AddField(
            model_name='cost',
            name='stone_income',
            field=models.IntegerField(default=25),
        ),
    ]
