# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .models import Video,Comment
from django.contrib import admin

# Register your models here.

admin.site.register(Video)
admin.site.register(Comment)
