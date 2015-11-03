from django.core.management.base import BaseCommand, CommandError
from django.utils import six
from rest_generator.helpers import *
from django.conf import settings
import os
import ast
import codegen

class Command(BaseCommand):
    help = 'setup project for django-rest-generator'


    def add_arguments(self, parser):
        pass


    def handle(self, *args, **options):
        print_bold("Welcome to django-rest-generator. Prepare project...")
        print(" base path : %s" % (settings.BASE_DIR))
        self.base_dir = settings.BASE_DIR
        self.app_dir = "%s/%s" % (settings.BASE_DIR, settings.BASE_DIR.split('/')[-1])
        
        self.init_api_routers()
        self.inject_into_main_urls()

    def init_api_routers(self):
        api_urls_file = open(os.path.join(self.app_dir,"api_urls.py"), "w")
        api_urls_file.write("from rest_framework import routers\nrouter = routers.SimpleRouter()")
        api_urls_file.close()
        print_ok("      api_urls.py - OK")

    def inject_into_main_urls(self):
        urls_ast = ast.parse(open(os.path.join(self.app_dir,"urls.py")).read())
        class MainUrlTransformer(ast.NodeTransformer):
            def visit_Assign(self, node):
                if node.targets[0].id == "urlpatterns":
                    print("find")
                    api_url_elt = ast.Call(args =["/api/v1"], func="url")
                    node.value.elts.insert(0,api_url_elt)
                return node
        
        MainUrlTransformer().visit(urls_ast)  
        print(ast.dump(urls_ast))