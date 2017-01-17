# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-01-13 17:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0007_post_dislikes'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserLikes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField(default=False, verbose_name='Нравится')),
                ('dislike', models.BooleanField(default=False, verbose_name='Не нравится')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Post', verbose_name='Статья')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'оценку пользователя',
                'verbose_name_plural': 'Оценки пользователей',
                'db_table': 'app_blog_user_likes',
            },
        ),
    ]