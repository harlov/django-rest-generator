import argparse
from rest_generator.helpers import *
from rest_generator.settings import *
import pip
from django.core import management as django_management

class Manager:
    def init_args(self):
        arg_parser = argparse.ArgumentParser(description='Django rest generator parser')
        
        arg_parser.add_argument('command', type=str, nargs='+', help='run command [startproject]')
        arg_parser.add_argument('name', type=str, nargs='+', help='project name')
        self.args = arg_parser.parse_args()

    def console_run(self):
        self.init_args()
        self.run_command()

    def install_packages(self):
        pip.main(['install', 'Django==%s' % (DJANGO_VERSION, )])
        pip.main(['install', 'djangorestframework==%s' % (DJANGO_REST_FRAMEWORK_VERSION, )])
        print_ok("required pip packages installed - OK")


    def run_command(self):
        if self.args.command[0] == 'startproject':
            self.run_startproject()
        else:
            print_fail("command '%s' not found!" % (self.args.command[0], ))

    def django_startproject(self):
        django_management.call_command('startproject', self.args.name[0])
        print_ok("'%s' project created - OK" % (self.args.name[0], ))

    def run_startproject(self):
        print_bold("init project %s " %(self.args.name[0], ))
        self.install_packages()
        self.django_startproject()

