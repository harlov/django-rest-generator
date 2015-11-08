from django.utils import six
from rest_generator.helpers import *
from django.core.management import call_command
import os
import ast
import astor
from django.conf import settings

class AppsConfiguratorService():
    def start(self, options):
        self.BASE_APP = settings.BASE_DIR.split('/')[-1]
        self.PROJECT_DIR = "%s/%s" % (settings.BASE_DIR, self.BASE_APP)
        self.APP_NAME = options['name']
        self.validate_name(self.APP_NAME)
        self.base_start_app()
        self.add_urls_file()
        self.inject_into_main_urls()
        print("Start app %s" % (self.APP_NAME, ) )

    def base_start_app(self):
        call_command('startapp', self.APP_NAME)

    def add_urls_file(self):
        urls_path = os.path.join(settings.BASE_DIR, self.APP_NAME, "urls.py")

        if os.path.exists(urls_path):
            return print_warn("  %s/urls.py is already exists - SKIP" %(self.APP_NAME, ))

        urls_file = open(urls_path, "w")
        
        write_lines = [
            "from words.views import *",
            "def setup_routes(root_route):",
            "    pass"
        ]

        urls_file.write('\n'.join(write_lines))
        urls_file.close()
        print_ok("  %s/urls.py - CREATED" %(self.APP_NAME, ))

    def inject_into_main_urls(self):
        urls_file = open(os.path.join(self.PROJECT_DIR,"api_urls.py"), "r+")
        urls_ast = ast.parse(urls_file.read())
        class ApiUrlTransformer(ast.NodeTransformer):
            def visit_Calc(self, node):
                print(dir(node))
                return node
        ApiUrlTransformer().visit(urls_ast)
        urls_ast.body.append(ast.Call(
                        func=ast.Name(id='url', ctx=ast.Load()),
                        args=[ast.Str('^api/v1'), 'include(api_urls.router.urls)'],
                        keywords = [], starargs=None, kwargs=None
                    )
        )

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