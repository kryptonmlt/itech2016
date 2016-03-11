# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0030_auto_20160311_1912'),
    ]

    operations = [
        migrations.CreateModel(
            name='MapInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('current_x_in_row', models.IntegerField(default=0)),
                ('current_y_row', models.IntegerField(default=5)),
            ],
        ),
    ]
