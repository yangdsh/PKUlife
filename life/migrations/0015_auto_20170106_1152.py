# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('life', '0014_friendship'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendship',
            name='person1',
            field=models.ForeignKey(related_name='person1', to='life.Person'),
        ),
        migrations.AlterField(
            model_name='friendship',
            name='person2',
            field=models.ForeignKey(related_name='person2', to='life.Person'),
        ),
    ]
