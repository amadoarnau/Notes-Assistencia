# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-10 15:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admincenter_files', '0014_auto_20170510_1539'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classe',
            name='professor',
        ),
        migrations.AddField(
            model_name='modul',
            name='professor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='admincenter_files.Professor'),
            preserve_default=False,
        ),
    ]