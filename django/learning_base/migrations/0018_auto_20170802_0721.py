# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-02 07:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning_base', '0017_multiplechoiceanswer_answer_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='multiplechoiceanswer',
            name='answer_image',
            field=models.CharField(default='', max_length=255, verbose_name='The Image for the answer'),
        ),
    ]
