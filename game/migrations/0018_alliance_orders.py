# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0017_auto_20160224_2308'),
    ]

    operations = [
        migrations.AddField(
            model_name='alliance',
            name='orders',
            field=models.CharField(default='', max_length=300),
            preserve_default=False,
        ),
    ]
