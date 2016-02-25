# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0024_remove_cost_war_machines_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='cost',
            name='war_machines_price',
            field=models.CharField(default=b'40,10,0', max_length=100),
        ),
    ]
