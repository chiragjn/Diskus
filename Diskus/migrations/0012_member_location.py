# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Diskus', '0011_auto_20150928_1826'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='location',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
