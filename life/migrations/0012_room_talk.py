# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('life', '0011_person_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='talk',
            field=models.TextField(blank=True),
        ),
    ]
