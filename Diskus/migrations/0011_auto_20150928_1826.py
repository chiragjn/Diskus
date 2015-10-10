# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Diskus', '0010_auto_20150927_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='profile_image_url',
            field=models.CharField(default=b'/static/image/user.png', max_length=1000, blank=True),
        ),
    ]
