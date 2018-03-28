# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-27 02:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import images.models
import images.storage


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0002_profileimage_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='profileimage',
            name='next_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='images.ProfileImage', verbose_name='Next Image'),
        ),
        migrations.AddField(
            model_name='profileimage',
            name='primary',
            field=models.BooleanField(default=False, verbose_name='Primary Image'),
        ),
        migrations.AlterField(
            model_name='profileimage',
            name='image',
            field=models.ImageField(storage=images.storage.OverwriteStorage(), upload_to=images.models.user_directory_path_profile, verbose_name='Image File'),
        ),
        migrations.AlterField(
            model_name='profileimage',
            name='status',
            field=models.CharField(choices=[('PEN', 'Pending'), ('APP', 'Approved'), ('REJ', 'Rejected')], default='PEN', max_length=3, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='profileimage',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
