# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0020_auto_20160225_1616'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cost',
            old_name='goldmines_price',
            new_name='gold_mines_price',
        ),
        migrations.RenameField(
            model_name='cost',
            old_name='lumbermills_price',
            new_name='lumber_mills_price',
        ),
        migrations.RenameField(
            model_name='cost',
            old_name='stonecaves_price',
            new_name='stone_caves_price',
        ),
    ]
