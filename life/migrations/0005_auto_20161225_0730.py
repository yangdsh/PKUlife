# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('life', '0004_auto_20161123_1202'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='slug1',
            field=models.CharField(max_length=30, blank=True),
        ),
        migrations.AddField(
            model_name='person',
            name='slug2',
            field=models.CharField(max_length=30, blank=True),
        ),
    ]
