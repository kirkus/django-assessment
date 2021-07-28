# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_assessment.utils


class Migration(migrations.Migration):

    dependencies = [
        ('django_assessment', '0003_add_response_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='response',
            name='file',
            field=models.FileField(max_length=255, blank=True, upload_to=django_assessment.utils.res_upload_to),
        ),
        migrations.AlterField(
            model_name='response',
            name='image',
            field=models.ImageField(max_length=255, blank=True, upload_to=django_assessment.utils.res_upload_to),
        ),
    ]
