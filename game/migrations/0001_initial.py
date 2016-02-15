# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=50)),
                ('surname', models.CharField(max_length=50)),
                ('picture', models.ImageField(default=b'pic_folder/None/no-img.jpg', upload_to=b'pic_folder/')),
                ('last_login_date', models.DateTimeField(verbose_name=b'date login')),
                ('last_attacked', models.DateTimeField(verbose_name=b'date attacked')),
                ('last_received_gold', models.DateTimeField(verbose_name=b'date received gold')),
                ('wins', models.IntegerField(default=0)),
                ('defeats', models.IntegerField(default=0)),
                ('alliance_owner', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Alliance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=300)),
                ('all_time_score', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='AllianceRequests',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=200)),
                ('date_occurred', models.DateTimeField(verbose_name=b'date occurred')),
                ('alliance_owner', models.ForeignKey(related_name='alliance_owner_account', to='game.Account')),
                ('from_account', models.ForeignKey(related_name='from_account_alliance_request', to='game.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('account', models.ForeignKey(to='game.Account')),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('gold', models.IntegerField(default=100)),
                ('supply', models.IntegerField(default=0)),
                ('walls_level', models.IntegerField(default=0)),
                ('footmen', models.IntegerField(default=0)),
                ('bowmen', models.IntegerField(default=0)),
                ('knights', models.IntegerField(default=0)),
                ('war_machines', models.IntegerField(default=0)),
                ('account', models.ForeignKey(to='game.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Cost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('footmen_price', models.IntegerField(default=10)),
                ('bowmen_price', models.IntegerField(default=15)),
                ('knights_price', models.IntegerField(default=25)),
                ('war_machines_price', models.IntegerField(default=50)),
                ('house_price', models.IntegerField(default=100)),
                ('wall_price', models.IntegerField(default=1000)),
                ('login_gold', models.IntegerField(default=100)),
            ],
        ),
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=200)),
                ('date_occurred', models.DateTimeField(verbose_name=b'date occurred')),
                ('city', models.ForeignKey(to='game.City')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=200)),
                ('date_occurred', models.DateTimeField(verbose_name=b'date occurred')),
                ('from_account', models.ForeignKey(related_name='from_account_messages', to='game.Account')),
                ('to_account', models.ForeignKey(related_name='to_account_messages', to='game.Account')),
            ],
        ),
        migrations.AddField(
            model_name='account',
            name='alliance',
            field=models.ForeignKey(to='game.Alliance'),
        ),
    ]
