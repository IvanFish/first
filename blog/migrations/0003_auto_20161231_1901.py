# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2016-12-31 16:01
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='text',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, default=''),
        ),
    ]
