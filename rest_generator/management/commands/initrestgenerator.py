from django.core.management.base import BaseCommand, CommandError
from django.utils import six
from rest_generator.helpers import *
from django.conf import settings
import os
import ast
import astor

class Command(BaseCommand):
    help = 'setup project for django-rest-generator'


    def add_arguments(self, parser):
        pass


    def handle(self, *args, **options):
        print_bold("Welcome to django-rest-generator. Prepare project...")
        print(" base path : %s" % (settings.BASE_DIR))
        self.base_dir = settings.BASE_DIR
        self.BASE_APP = settings.BASE_DIR.split('/')[-1]
        self.APP_DIR = "%s/%s" % (settings.BASE_DIR, self.BASE_APP)
        
        self.init_api_routers()
        self.inject_into_main_urls()

    def init_api_routers(self):
        api_urls_file = open(os.path.join(self.APP_DIR,"api_urls.py"), "w")
        api_urls_file.write("from rest_framework import routers\nrouter = routers.SimpleRouter()")
        api_urls_file.close()
        print_ok("      %s/api_urls.py - CREATED" %(self.BASE_APP, ))

    def inject_into_main_urls(self):
        urls_file = open(os.path.join(self.APP_DIR,"urls.py"), "r+")
        urls_ast = ast.parse(urls_file.read())
        class MainUrlTransformer(ast.NodeTransformer):
            def visit_Assign(self, node):
                if node.targets[0].id == "urlpatterns":
                    api_url_elt = ast.Call(
                        func=ast.Name(id='url', ctx=ast.Load()),
                        args=[ast.Str('/api/v1'), 'include(api_urls.router.urls)'],
                        keywords = [], starargs=None, kwargs=None
                    )
                    api_url_elt.lineno = 5                    
                    node.value.elts.insert(2,api_url_elt)
                return node
            # def visit_ImportFrom(self, node):
            #     print("Import")
            #     print(node)
            #     return node

        urls_ast.body.insert(0, ast.Import(
            names=[
                ast.alias(name='%s.api_urls' % (self.BASE_APP,), asname='api_urls')
            ]
            )
        )

        
        MainUrlTransformer().visit(urls_ast)
        ast.fix_missing_locations(urls_ast)
        
        urls_file.seek(0)
        urls_file.write(astor.to_source(urls_ast, add_line_information=False))
        urls_file.truncate()
        urls_file.close()
        print_ok("      %s/urls.py - MODIFIED" %(self.BASE_APP, ))