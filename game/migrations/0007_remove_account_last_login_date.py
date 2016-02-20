# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0006_auto_20160216_0033'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='last_login_date',
        ),
    ]
