# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-15 12:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stationnement', '0002_auto_20170515_1337'),
    ]

    operations = [
        migrations.AddField(
            model_name='parking',
            name='couvert',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parking',
            name='etage',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parking',
            name='numero',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]