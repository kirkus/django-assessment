# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_assessment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='help_text',
            field=models.CharField(max_length=256, blank=True),
        ),
        migrations.AddField(
            model_name='question',
            name='placeholder',
            field=models.CharField(max_length=128, blank=True),
        ),
    ]
