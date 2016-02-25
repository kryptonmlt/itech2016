# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0021_auto_20160225_1633'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllianceMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=200)),
                ('date_occurred', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date occurred')),
                ('from_account', models.ForeignKey(related_name='from_account_alliance_messages', to='game.Account')),
                ('to_alliance', models.ForeignKey(related_name='to_alliance_messages', to='game.Alliance')),
            ],
        ),
    ]
