# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('life', '0002_auto_20161123_0352'),
    ]

    operations = [
        migrations.CreateModel(
            name='source',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to='static', blank=True)),
                ('text', models.TextField(blank=True)),
                ('version', models.FloatField(default=1, blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='membership',
            name='invite_person',
        ),
        migrations.AddField(
            model_name='membership',
            name='allowed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='membership',
            name='application',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='room',
            name='creator',
            field=models.ForeignKey(default=0, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='person',
            name='portrait',
            field=models.ImageField(upload_to='media', blank=True),
        ),
    ]
