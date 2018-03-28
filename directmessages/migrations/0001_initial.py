# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-17 17:49
from __future__ import unicode_literals

import directmessages.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0004_user_blocked_users'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_type', models.CharField(choices=[('txt', 'Text'), ('img', 'Image')], max_length=3)),
                ('recipient_content', models.TextField(blank=True, null=True, verbose_name='Content')),
                ('sender_content', models.TextField(blank=True, null=True, verbose_name='Content (Translated)')),
                ('image', models.ImageField(blank=True, null=True, upload_to=directmessages.models.user_directory_path_profile, verbose_name='Image Content')),
                ('sent_at', models.DateTimeField(blank=True, null=True, verbose_name='sent at')),
                ('read_at', models.DateTimeField(blank=True, null=True, verbose_name='read at')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_dm', to=settings.AUTH_USER_MODEL, verbose_name='Recipient')),
                ('recipient_language', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recipient_language', to='core.Language', verbose_name='Recipient Language')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_dm', to=settings.AUTH_USER_MODEL, verbose_name='Sender')),
                ('sender_language', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='source_language', to='core.Language', verbose_name='Source Language')),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
            },
        ),
    ]
