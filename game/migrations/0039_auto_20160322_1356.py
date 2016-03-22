# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0038_remove_map_x'),
    ]

    operations = [
        migrations.AlterField(
            model_name='map',
            name='value',
            field=models.CharField(max_length=5000),
        ),
    ]
