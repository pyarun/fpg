# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from address.models import Country
from iso3166 import countries

from django.db import models, migrations

class Migration(migrations.Migration):
    """
        This will insert all the countries initially in database
    """
    def setup_countries(apps, schema_editor):

        for country in countries:
            if(len(country.name) < 40):
                item, created = Country.objects.get_or_create(name=country.name, code=country.alpha2)
                item.save()
    dependencies = [
        ('facility', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(setup_countries)
    ]
