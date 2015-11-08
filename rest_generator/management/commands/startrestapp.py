from django.core.management.base import BaseCommand, CommandError

from rest_generator.services import AppsConfiguratorService

class Command(BaseCommand):
    help = 'startapp for restframework'


    def add_arguments(self, parser):
        parser.add_argument('name', help='Name of the application.')


    def handle(self, *args, **options):
        apps_service = AppsConfiguratorService()
        apps_service.start(options)
    