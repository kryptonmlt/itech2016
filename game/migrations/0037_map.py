# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0036_auto_20160322_1252'),
    ]

    operations = [
        migrations.CreateModel(
            name='Map',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('x', models.IntegerField(default=0)),
                ('y', models.IntegerField(default=0)),
                ('value', models.IntegerField(default=0)),
            ],
        ),
    ]
