# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0037_map'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='map',
            name='x',
        ),
    ]
