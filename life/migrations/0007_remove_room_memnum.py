# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('life', '0006_auto_20161225_0857'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='memnum',
        ),
    ]
