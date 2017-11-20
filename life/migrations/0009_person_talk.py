# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('life', '0008_person_rnum'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='talk',
            field=models.TextField(blank=True),
        ),
    ]
