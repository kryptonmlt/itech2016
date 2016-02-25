# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0021_auto_20160225_1633'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='food',
        ),
        migrations.RemoveField(
            model_name='city',
            name='houses_level',
        ),
        migrations.RemoveField(
            model_name='cost',
            name='houses_price',
        ),
        migrations.RemoveField(
            model_name='cost',
            name='login_gold',
        ),
        migrations.AlterField(
            model_name='cost',
            name='farms_price',
            field=models.CharField(default=b'200,100,100', max_length=100),
        ),
        migrations.AlterField(
            model_name='cost',
            name='gold_mines_price',
            field=models.CharField(default=b'300,150,150', max_length=100),
        ),
        migrations.AlterField(
            model_name='cost',
            name='lumber_mills_price',
            field=models.CharField(default=b'200,200,100', max_length=100),
        ),
        migrations.AlterField(
            model_name='cost',
            name='stone_caves_price',
            field=models.CharField(default=b'200,150,150', max_length=100),
        ),
        migrations.AlterField(
            model_name='cost',
            name='wall_price',
            field=models.CharField(default=b'1000,100,200', max_length=100),
        ),
        migrations.AlterField(
            model_name='cost',
            name='war_machines_price',
            field=models.IntegerField(default=40),
        ),
    ]
