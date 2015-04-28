from __future__ import unicode_literals

from django.db import models, migrations
from utils.models import Sports

SPORTS = [
            'Archery', 'Badminton', 'Baseball', 'Bowling', 'Boxing', 'Chess', 'Cricket',
            'Football', 'Golf', 'Hockey', 'Basketball', 'Table Tennis', 'Tennis',
            'Rock Climbing', 'Shooting', 'Snooker', 'Swimming', 'Volleyball'
          ]

class Migration(migrations.Migration):
    """
        This will insert initial data in Sports table
    """
    def setup_sports(apps, schema_editor):
        for sport in SPORTS:
            item, created = Sports.objects.get_or_create(name=sport)
            item.save()

    dependencies = [
        ('utils', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(setup_sports)
    ]