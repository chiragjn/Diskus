# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Diskus', '0008_auto_20150927_0641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='profile_image_url',
            field=models.CharField(default=b'/static/image/user.png', max_length=100, blank=True),
        ),
    ]
