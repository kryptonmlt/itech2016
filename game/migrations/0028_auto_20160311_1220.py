# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0027_auto_20160226_2359'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='x',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='city',
            name='y',
            field=models.IntegerField(default=0),
        ),
    ]
