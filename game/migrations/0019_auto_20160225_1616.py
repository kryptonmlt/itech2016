# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0018_alliance_orders'),
    ]

    operations = [
        migrations.RenameField(
            model_name='city',
            old_name='lands_owned',
            new_name='farms',
        ),
        migrations.RenameField(
            model_name='city',
            old_name='house_level',
            new_name='houses_level',
        ),
        migrations.RenameField(
            model_name='cost',
            old_name='lands_price',
            new_name='farms_price',
        ),
        migrations.AddField(
            model_name='city',
            name='food',
            field=models.IntegerField(default=100),
        ),
        migrations.AddField(
            model_name='city',
            name='gold_mines',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='city',
            name='lumber',
            field=models.IntegerField(default=100),
        ),
        migrations.AddField(
            model_name='city',
            name='lumber_mills',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='city',
            name='stone_caves',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='city',
            name='stones',
            field=models.IntegerField(default=100),
        ),
        migrations.AddField(
            model_name='cost',
            name='goldmines_price',
            field=models.IntegerField(default=500),
        ),
        migrations.AddField(
            model_name='cost',
            name='lumbermills_price',
            field=models.IntegerField(default=500),
        ),
        migrations.AddField(
            model_name='cost',
            name='stonecaves_price',
            field=models.IntegerField(default=500),
        ),
    ]
