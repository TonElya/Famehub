# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
import django


# Create your models here.
STATUS_CHOICES = (('d', 'Draft'),('p', 'Published'),('w', 'Withdrawn'),)
class Video(models.Model):
    title = models.CharField(max_length=250, null=True,unique = True)
    vid_desc = models.CharField(max_length=1000, null=True,unique = False)
    #lesson_img = models.ImageField(upload_to="accounts/static/lessons/uploads", null=True, blank=True)
    video = models.FileField(upload_to="static/tube/uploads", null=True,blank=True)
    link = models.URLField(null=True,blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank = True, on_delete = models.SET_NULL)
    date_created = models.DateTimeField(default=django.utils.timezone.now)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='d')
    views = models.IntegerField(null=True)

