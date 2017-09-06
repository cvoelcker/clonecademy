# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-16 09:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning_base', '0003_informationtext_text_field'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='informationtext',
            name='visible',
        ),
        migrations.AddField(
            model_name='informationtext',
            name='question_image',
            field=models.TextField(blank=True),
        ),
    ]