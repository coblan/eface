from django.contrib import admin

# Register your models here.
from . import js_cfg
from django.conf import settings
from helpers.func.dot_dict import read_dict_path
if read_dict_path( settings,'DATABASES.ENGINE') =='django.contrib.gis.db.backends.postgis':
    from .field_proc import point_proc