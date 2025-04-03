from django.contrib import admin

# Register your models here.
from . import js_cfg
from django.conf import settings
from helpers.func.dot_dict import read_dict_path
if read_dict_path( settings,'DATABASES.default.ENGINE') in ['django.contrib.gis.db.backends.postgis','django.contrib.gis.db.backends.mysql']:
    from .field_proc import point_proc
    from . field_proc import polygen_proc