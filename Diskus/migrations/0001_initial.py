# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(unique=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ImageUploads',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('img', models.ImageField(default=b'pic_folder/None/no-img.jpg', upload_to=b'pic_folder/')),
                ('name', models.CharField(default=None, max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('profile_image_url', models.CharField(default=b'/static/image/user.png', max_length=1000, blank=True)),
                ('type', models.IntegerField(default=0)),
                ('date_of_birth', models.DateField(auto_now=True)),
                ('details_visible', models.BooleanField(default=True)),
                ('bio', models.CharField(default=None, max_length=500)),
                ('slug', models.SlugField(unique=True, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
                ('visible', models.BooleanField(default=True)),
                ('author', models.ForeignKey(to='Diskus.Member')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(max_length=500)),
                ('resolved', models.BooleanField(default=False)),
                ('member', models.ForeignKey(to='Diskus.Member')),
                ('post', models.ForeignKey(to='Diskus.Post')),
            ],
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pinned', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=100)),
                ('locked', models.BooleanField(default=False)),
                ('visible', models.BooleanField(default=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(unique=True, blank=True)),
                ('category', models.ForeignKey(default=None, to='Diskus.Category')),
                ('moderator', models.ForeignKey(related_name='moderator_set', blank=True, to='Diskus.Member', null=True)),
                ('op', models.ForeignKey(related_name='op_set', to='Diskus.Member')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='thread',
            field=models.ForeignKey(to='Diskus.Thread'),
        ),
    ]
