# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-10 15:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admincenter_files', '0004_classe'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alumne',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200)),
            ],
        ),
    ]