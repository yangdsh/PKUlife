# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('life', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='person',
            old_name='dsrp',
            new_name='dscrp',
        ),
        migrations.AlterField(
            model_name='membership',
            name='date_joined',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='membership',
            name='invite_person',
            field=models.CharField(max_length=30, blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='credit',
            field=models.FloatField(default=1, blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='gender',
            field=models.CharField(default='U', max_length=2, blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('U', 'unKnown')]),
        ),
        migrations.AlterField(
            model_name='person',
            name='gps',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='slug',
            field=models.CharField(default='life', max_length=30, blank=True),
        ),
    ]
