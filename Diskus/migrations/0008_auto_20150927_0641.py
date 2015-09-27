# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Diskus', '0007_thread_last_modified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thread',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
