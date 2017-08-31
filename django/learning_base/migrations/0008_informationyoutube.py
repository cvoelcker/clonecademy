# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-28 17:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('learning_base', '0007_auto_20170822_1048'),
    ]

    operations = [
        migrations.CreateModel(
            name='InformationYoutube',
            fields=[
                ('question_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='learning_base.Question')),
                ('url', models.TextField(blank=True)),
                ('text_field', models.TextField()),
            ],
            options={
                'abstract': False,
            },
            bases=('learning_base.question',),
        ),
    ]
