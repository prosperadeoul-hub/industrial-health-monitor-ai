from django.core.management.base import BaseCommand

from monitoring.models import SystemComponent


class Command(BaseCommand):
    help = 'Seed demo data'

    def handle(self, *args, **options):
        SystemComponent.objects.get_or_create(name='demo-server', defaults={'component_type': 'server'})
        self.stdout.write('Seeded')
