# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('life', '0012_room_talk'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='gps',
            field=models.CharField(max_length=50, blank=True),
        ),
    ]
