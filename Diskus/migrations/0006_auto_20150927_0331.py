# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Diskus', '0005_auto_20150927_0325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thread',
            name='moderator',
            field=models.ForeignKey(related_name='moderator_set', blank=True, to='Diskus.Member', null=True),
        ),
    ]
