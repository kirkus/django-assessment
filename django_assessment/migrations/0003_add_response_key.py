# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('django_assessment', '0002_add_help_text_placeholder'),
    ]

    operations = [
        migrations.AddField(
            model_name='response',
            name='key',
            field=models.CharField(max_length=128, blank=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='response',
            name='user',
            field=models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
