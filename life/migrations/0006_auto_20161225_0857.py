# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('life', '0005_auto_20161225_0730'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='closed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='room',
            name='memnum',
            field=models.FloatField(default=0),
        ),
    ]
