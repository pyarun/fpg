# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('address', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, null=True, blank=True)),
                ('date', models.DateField(help_text=b'Booking date')),
                ('start_time', models.TimeField(help_text=b'start time of booking')),
                ('end_time', models.TimeField(help_text=b'end time of booking')),
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
                ('contact_number', models.CharField(max_length=12)),
                ('description', models.TextField(null=True, blank=True)),
                ('address', models.OneToOneField(to='address.Address')),
                ('owner', models.ForeignKey(help_text=b'Owner of the club', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(help_text=b'Type of ground or resource', max_length=100, null=True, blank=True)),
                ('open_time', models.TimeField(help_text=b'Time from which resource is available')),
                ('close_time', models.TimeField(help_text=b'Time up to resource is available')),
                ('fee', models.PositiveIntegerField(help_text=b'Cost of the resource per hour')),
                ('photo', models.ImageField(null=True, upload_to=b'resources', blank=True)),
                ('status', models.CharField(default=b'available', help_text=b'Status of resource whether it is available for booking or not', max_length=32, choices=[(b'available', b'Available'), (b'unavailable', b'Unavailable')])),
                ('description', models.TextField(null=True, blank=True)),
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
        migrations.AddField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
