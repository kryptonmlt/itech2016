# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0033_auto_20160321_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='lumber',
            field=models.IntegerField(default=1000),
        ),
        migrations.AlterField(
            model_name='city',
            name='stones',
            field=models.IntegerField(default=1000),
        ),
    ]
