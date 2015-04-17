# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('utils', '0001_initial'),
        ('address', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, null=True, blank=True)),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('contact_number', models.CharField(max_length=12, null=True, blank=True)),
                ('description', models.CharField(max_length=400, null=True, blank=True)),
                ('address', models.OneToOneField(null=True, blank=True, to='address.Address')),
                ('owner', models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, null=True, blank=True)),
                ('type', models.CharField(max_length=100, null=True, blank=True)),
                ('open_time', models.TimeField(null=True, blank=True)),
                ('close_time', models.TimeField(null=True, blank=True)),
                ('fees', models.PositiveIntegerField()),
                ('photo', models.ImageField(upload_to=b'resources')),
                ('status', models.CharField(default=b'available', max_length=32, choices=[(b'available', b'Available'), (b'unavailable', b'Unavailable')])),
                ('description', models.CharField(max_length=400, null=True, blank=True)),
                ('club', models.ForeignKey(to='facility.Club')),
                ('sport', models.ForeignKey(to='utils.Sports')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='booking',
            name='resource',
            field=models.ForeignKey(to='facility.Resource'),
            preserve_default=True,
        ),
    ]
