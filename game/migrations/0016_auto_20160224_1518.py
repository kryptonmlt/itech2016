# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0015_auto_20160224_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='citygraphic',
            name='picture',
            field=models.ImageField(upload_to=b'city', blank=True),
        ),
    ]
