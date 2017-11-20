# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django import forms
from django.contrib.auth.models import User

GENDER_CHOICES = (
        (u'M', u'Male'),
        (u'F', u'Female'),
        (u'U', u'unKnown'),
)

class Person(models.Model):                        
    name = models.CharField(max_length=30)
    dscrp = models.TextField(blank=True)
    credit = models.FloatField(default=8, blank=True)
    bad = models.FloatField(default=0, blank=True)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, default='U', blank=True) 
    rnum = models.FloatField(default=0)
    gps = models.CharField(max_length=50, blank=True)
    talk = models.TextField(blank=True)
    token = models.TextField(blank=True)
    portrait = models.ImageField(upload_to='media', blank=True)
    slug1 = models.CharField(max_length=30, blank=True)
    slug2 = models.CharField(max_length=30, blank=True)
    user = models.OneToOneField(User,verbose_name=('用户'),blank=True)
    def __unicode__(self):                         
        return self.name

class Room(models.Model):
    name = models.CharField(max_length=30)
    slug = models.CharField(max_length=30, default='life', blank=True)
    date = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=300, blank=True)
    gps = models.CharField(max_length=50, blank=True)
    dscrp = models.TextField(blank=True)
    talk = models.TextField(blank=True)
    closed = models.BooleanField(default=False)
    members = models.ManyToManyField(Person, through='Membership')
    creator = models.ForeignKey(User)

    def __unicode__(self):
        return self.name

class Membership(models.Model):
    person = models.ForeignKey(Person)
    room = models.ForeignKey(Room)
    date_joined = models.CharField(max_length=30, blank=True)
    application = models.TextField(blank=True)
    allowed = models.BooleanField(default=False)
    rate = models.FloatField(blank=True, default=1)
    evaluate = models.TextField(blank=True)
    
class Friendship(models.Model):
    person1 = models.ForeignKey(Person, related_name='person1')
    person2 = models.ForeignKey(Person, related_name='person2')
    rated = models.FloatField(default=0)
    
class source(models.Model):
    image = models.ImageField(upload_to='static', blank=True)
    text = models.TextField(blank=True)
    version = models.FloatField(default=1, blank=True)
