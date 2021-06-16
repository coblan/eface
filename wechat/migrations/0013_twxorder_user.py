# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2021-06-16 22:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wechat', '0012_wxinfo_session_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='twxorder',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
