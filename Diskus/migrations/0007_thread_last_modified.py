# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.datetime_safe


class Migration(migrations.Migration):

    dependencies = [
        ('Diskus', '0006_auto_20150927_0331'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='last_modified',
            field=models.DateTimeField(default=django.utils.datetime_safe.datetime.now, auto_now_add=True),
            preserve_default=False,
        ),
    ]
