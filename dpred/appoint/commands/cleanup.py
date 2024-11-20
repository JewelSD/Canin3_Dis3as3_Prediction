# yourapp/management/commands/cleanup.py

from django.core.management.base import BaseCommand
from datetime import timedelta
from django.utils import timezone
from appoint.models import appointment


class Command(BaseCommand):
    help = 'Deletes appointment records older than two days'

    def handle(self, *args, **kwargs):
        two_days_ago = timezone.now() - timedelta(days=2)
        appointment.objects.filter(date__lt=two_days_ago).delete()
        self.stdout.write(self.style.SUCCESS(
            'Successfully deleted old appointments'))
