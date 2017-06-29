# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-20 13:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('learning_base', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='modrequest',
            options={'ordering': ['date']},
        ),
        migrations.AlterField(
            model_name='question',
            name='module',
            field=models.ForeignKey(help_text='The corresponding module for the question', on_delete=django.db.models.deletion.CASCADE, to='learning_base.Module', verbose_name='Module'),
        ),
    ]