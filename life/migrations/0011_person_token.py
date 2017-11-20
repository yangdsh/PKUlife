# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('life', '0010_auto_20170105_0916'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='token',
            field=models.TextField(blank=True),
        ),
    ]
