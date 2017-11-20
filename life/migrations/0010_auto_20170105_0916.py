# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('life', '0009_person_talk'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='bad',
            field=models.FloatField(default=0, blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='credit',
            field=models.FloatField(default=8, blank=True),
        ),
    ]
