# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0031_mapinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='alliance',
            name='slug',
            field=models.SlugField(default=''),
            preserve_default=False,
        ),
    ]
