# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-04-20 02:51
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import helpers.director.model_func.cus_fields.cus_picture


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0003_twxorder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wxinfo',
            name='head',
            field=helpers.director.model_func.cus_fields.cus_picture.PictureField(blank=True, max_length=300, verbose_name='微信头像'),
        ),
        migrations.AlterField(
            model_name='wxinfo',
            name='nickname',
            field=models.CharField(blank=True, max_length=200, verbose_name='微信昵称'),
        ),
        migrations.AlterField(
            model_name='wxinfo',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户账号'),
        ),
    ]
