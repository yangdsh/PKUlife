# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('life', '0007_remove_room_memnum'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='rnum',
            field=models.FloatField(default=0),
        ),
    ]
