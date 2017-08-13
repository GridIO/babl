# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-13 02:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import images.models
import images.storage
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(storage=images.storage.OverwriteStorage(), upload_to=images.models.user_directory_path_profile)),
                ('order', models.IntegerField()),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProfileImage',
            fields=[
                ('image_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='images.Image')),
            ],
            bases=('images.image',),
        ),
        migrations.AddField(
            model_name='image',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
