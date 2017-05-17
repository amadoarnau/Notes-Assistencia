# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-04 15:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Modul',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_modul', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Nota',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nota_nota', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='UF',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_uf', models.CharField(max_length=200)),
                ('nom_modul_nota', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admincenter_files.Modul')),
            ],
        ),
        migrations.CreateModel(
            name='Usuari',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username_usuari', models.CharField(max_length=200)),
                ('password_usuari', models.CharField(max_length=200)),
                ('dni_usuari', models.CharField(max_length=9)),
            ],
        ),
        migrations.AddField(
            model_name='nota',
            name='dni_usuari_nota',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admincenter_files.Usuari'),
        ),
        migrations.AddField(
            model_name='nota',
            name='nom_modul_nota',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admincenter_files.Modul'),
        ),
        migrations.AddField(
            model_name='nota',
            name='uf_nota',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admincenter_files.UF'),
        ),
    ]
