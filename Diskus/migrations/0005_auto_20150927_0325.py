# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Diskus', '0004_auto_20150927_0323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(unique=True, blank=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='slug',
            field=models.SlugField(unique=True, blank=True),
        ),
        migrations.AlterField(
            model_name='thread',
            name='slug',
            field=models.SlugField(unique=True, blank=True),
        ),
    ]
