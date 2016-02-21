# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0007_remove_account_last_login_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alliancerequest',
            name='date_occurred',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name=b'date occurred'),
        ),
    ]
