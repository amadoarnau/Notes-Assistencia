# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-10 15:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admincenter_files', '0012_auto_20170510_1528'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alumne',
            name='classe',
        ),
        migrations.DeleteModel(
            name='Alumne',
        ),
        migrations.DeleteModel(
            name='Classe',
        ),
    ]