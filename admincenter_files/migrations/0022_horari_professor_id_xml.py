# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-12 15:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admincenter_files', '0021_auto_20170512_1435'),
    ]

    operations = [
        migrations.AddField(
            model_name='horari',
            name='professor_id_xml',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
