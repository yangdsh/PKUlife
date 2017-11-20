# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('life', '0013_room_gps'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friendship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rated', models.FloatField(default=0)),
                ('person1', models.OneToOneField(related_name='person1', to='life.Person')),
                ('person2', models.OneToOneField(related_name='person2', to='life.Person')),
            ],
        ),
    ]
