from django.core.management.base import BaseCommand, CommandError
from django.utils import six
from rest_generator.services import BaseProjectConfiguratorService

class Command(BaseCommand):
    help = 'setup project for django-rest-generator'


    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        configurator_service = BaseProjectConfiguratorService()
        configurator_service.start()
