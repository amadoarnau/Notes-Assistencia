# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-10 15:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('admincenter_files', '0007_alumne'),
    ]

    operations = [
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200)),
                ('dni', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='classe',
            name='professor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admincenter_files.Professor'),
            preserve_default=False,
        ),
    ]
