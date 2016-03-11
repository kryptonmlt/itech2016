# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0029_delete_citygraphic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='farms',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='city',
            name='gold_mines',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='city',
            name='lumber_mills',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='city',
            name='stone_caves',
            field=models.IntegerField(default=1),
        ),
    ]
