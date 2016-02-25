# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0025_cost_war_machines_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cost',
            name='war_machines_price',
            field=models.CharField(default=b'40,10', max_length=100),
        ),
    ]
