# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-16 17:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admincenter_files', '0036_llico_classe'),
    ]

    operations = [
        migrations.AddField(
            model_name='alumne',
            name='cognom',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]