# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import chartbuilder.models
import django.utils.timezone
from django.conf import settings

try:
    from cms.models.pluginmodel import CMSPlugin
except ImportError:
    CMSPlugin = None


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL)
    ]
    if CMSPlugin is not None:
        dependencies += [
            ('cms', '0012_auto_20150607_2207'),
        ]

    operations = [
        migrations.CreateModel(
            name='Chart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('csv_data', models.TextField(blank=True)),
                ('chart_settings', jsonfield.fields.JSONField(blank=True)),
                ('width', models.IntegerField(null=True, blank=True)),
                ('height', models.IntegerField(null=True, blank=True)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
                ('svg', models.FileField(null=True, upload_to=chartbuilder.models.chart_file_path, blank=True)),
                ('customised', models.BooleanField(default=False)),
                ('is_public', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('-created_at',),
                'verbose_name': 'chart',
                'verbose_name_plural': 'charts',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DisplayChartPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('chart', models.ForeignKey(to='chartbuilder.Chart')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.AlterField(
            model_name='chart',
            name='svg',
            field=models.FileField(storage=chartbuilder.models.OverwriteStorage(), null=True, upload_to=chartbuilder.models.chart_file_path, blank=True),
            preserve_default=True,
        ),
    ]
