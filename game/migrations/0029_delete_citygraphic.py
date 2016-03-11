# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0028_auto_20160311_1220'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CityGraphic',
        ),
    ]
