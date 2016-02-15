# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllianceRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=200)),
                ('date_occurred', models.DateTimeField(verbose_name=b'date occurred')),
                ('alliance_owner', models.ForeignKey(related_name='alliance_owner_account', to='game.Account')),
                ('from_account', models.ForeignKey(related_name='from_account_alliance_request', to='game.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=200)),
                ('date_occurred', models.DateTimeField(verbose_name=b'date occurred')),
                ('city', models.ForeignKey(to='game.City')),
            ],
        ),
        migrations.RemoveField(
            model_name='alliancerequests',
            name='alliance_owner',
        ),
        migrations.RemoveField(
            model_name='alliancerequests',
            name='from_account',
        ),
        migrations.RemoveField(
            model_name='logs',
            name='city',
        ),
        migrations.DeleteModel(
            name='AllianceRequests',
        ),
        migrations.DeleteModel(
            name='Logs',
        ),
    ]
