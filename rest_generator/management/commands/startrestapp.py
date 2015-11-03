from django.core.management.base import BaseCommand, CommandError
from django.utils import six

class Command(BaseCommand):
    help = 'startapp for restframework'


    def add_arguments(self, parser):
        parser.add_argument('name', help='Name of the application.')


    def handle(self, *args, **options):
        self.app_name = options['name']
        self.validate_name(self.app_name)
        print("Start app %s" % (self.app_name, ) )

    def validate_name(self, name):
        if name is None:
                raise CommandError("you must provide name")
        if six.PY2:
            if not re.search(r'^[_a-zA-Z]\w*$', name):
                if not re.search(r'^[_a-zA-Z]', name):
                    message = 'make sure the name begins with a letter or underscore'
                else:
                    message = 'use only numbers, letters and underscores'
                raise CommandError("%r is not a valid name. Please %s." %
                                           (name, message))
        else:
            if not name.isidentifier():
                raise CommandError(
                        "%r is not a valid name. Please make sure the name is "
                        "a valid identifier." % (name, )
                    )