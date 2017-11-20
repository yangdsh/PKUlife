# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_joined', models.DateField()),
                ('invite_person', models.CharField(max_length=30)),
                ('rate', models.FloatField(default=1, blank=True)),
                ('evaluate', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('dsrp', models.TextField(blank=True)),
                ('credit', models.FloatField(default=1)),
                ('gender', models.CharField(default='U', max_length=2, choices=[('M', 'Male'), ('F', 'Female'), ('U', 'unKnown')])),
                ('gps', models.CharField(max_length=50)),
                ('portrait', models.ImageField(upload_to='photo', blank=True)),
                ('user', models.OneToOneField(verbose_name='\u7528\u6237', blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('slug', models.CharField(default='life', max_length=30)),
                ('date', models.CharField(max_length=30, blank=True)),
                ('address', models.CharField(max_length=300, blank=True)),
                ('dscrp', models.TextField(blank=True)),
                ('members', models.ManyToManyField(to='life.Person', through='life.Membership')),
            ],
        ),
        migrations.AddField(
            model_name='membership',
            name='person',
            field=models.ForeignKey(to='life.Person'),
        ),
        migrations.AddField(
            model_name='membership',
            name='room',
            field=models.ForeignKey(to='life.Room'),
        ),
    ]
