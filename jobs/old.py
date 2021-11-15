# purge_old_data.py

from django.core.management.base import BaseCommand, CommandError
from .models import *
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Delete objects older than 10 days'

    def handle(self, *args, **options):
        Job.objects.filter(create_at__lte=datetime.now()-timedelta(days=21)).delete()
        self.stdout.write('Deleted objects older than 10 days')
