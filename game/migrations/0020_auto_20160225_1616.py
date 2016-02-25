# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0019_auto_20160225_1616'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cost',
            old_name='house_price',
            new_name='houses_price',
        ),
    ]
