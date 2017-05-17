# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-10 15:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admincenter_files', '0009_auto_20170510_1510'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alumne',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200)),
                ('dni', models.CharField(max_length=200)),
                ('classe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admincenter_files.Classe')),
            ],
        ),
    ]
