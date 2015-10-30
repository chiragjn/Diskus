# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Diskus', '0012_member_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='banned',
            field=models.BooleanField(default=False),
        ),
    ]
