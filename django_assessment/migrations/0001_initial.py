# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_assessment.utils
from django.conf import settings


def forwards(apps, schema_editor):
    QuestionType = apps.get_model("django_assessment", "QuestionType")
    QuestionType.objects.bulk_create([
        QuestionType(name='Radio Button', slug='radio-button'),
        QuestionType(name='Checkbox', slug='checkbox'),
        QuestionType(name='Dropdown', slug='dropdown'),
        QuestionType(name='Long Text', slug='long-text'),
        QuestionType(name='Short Text', slug='short-text'),
        QuestionType(name='Image Upload', slug='image'),
        QuestionType(name='File Upload', slug='file')
    ])


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Assessment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=128, unique=True)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('text', models.TextField(help_text='"The text of the option.')),
                ('value', models.IntegerField(help_text='"The value of the option.')),
                ('order', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='OptionSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=128, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.TextField()),
                ('varname', models.CharField(max_length=64, help_text='The name to use in order to build the form field.')),
                ('is_required', models.BooleanField(default=False, help_text='Check this if question is required.')),
                ('order', models.IntegerField(default=0)),
                ('assessment', models.ForeignKey(related_name='questions', to='django_assessment.Assessment')),
                ('option_set', models.ForeignKey(blank=True, null=True, to='django_assessment.OptionSet')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='QuestionType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=64, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('answer', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, upload_to=django_assessment.utils.res_upload_to)),
                ('file', models.FileField(blank=True, upload_to=django_assessment.utils.res_upload_to)),
                ('assessment', models.ForeignKey(related_name='responses', to='django_assessment.Assessment')),
                ('question', models.ForeignKey(to='django_assessment.Question')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='type',
            field=models.ForeignKey(to='django_assessment.QuestionType'),
        ),
        migrations.AddField(
            model_name='option',
            name='option_set',
            field=models.ForeignKey(related_name='options', to='django_assessment.OptionSet'),
        ),
        migrations.AlterUniqueTogether(
            name='question',
            unique_together=set([('assessment', 'varname')]),
        ),
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
