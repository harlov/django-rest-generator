from rest_generator.helpers import *
import rest_generator.settings as generator_settings
from django.conf import settings
from yapf.yapflib.yapf_api import FormatCode
import os
import ast
import astor



class BaseProjectConfiguratorService:

    def start(self):
        print_bold("Welcome to django-rest-generator. Prepare project...")
        
        
        self.request_configuration()

        self.init_requirements()
        self.init_api_routers()
        self.inject_into_main_urls()

    def request_configuration(self):
        base_dir = input(
            get_bold(
                '%s (default: %s) --> ' % (
                    get_bold('base project directory'),
                    settings.BASE_DIR, 
                )
            )
        )
        if len(base_dir):
            self.base_dir = base_dir
        else:
            self.base_dir = settings.BASE_DIR

        print(" base path : %s" % (self.base_dir, ))

        self.BASE_APP = settings.BASE_DIR.split('/')[-1]
        self.PROJECT_DIR = "%s/%s" % (settings.BASE_DIR, self.BASE_APP)        

    def init_api_routers(self):
        api_urls_path = os.path.join(self.PROJECT_DIR,"api_urls.py")

        if os.path.exists(api_urls_path):
            return print_warn("  api_urls.py is already exists - SKIP")

        api_urls_file = open(api_urls_path, "w")
        api_urls_file.write("from rest_framework import routers\n\nrouter = routers.SimpleRouter()")
        api_urls_file.close()
        print_ok("  %s/api_urls.py - CREATED" %(self.BASE_APP, ))

    def inject_into_main_urls(self):
        urls_file = open(os.path.join(self.PROJECT_DIR,"urls.py"), "r+")
        urls_ast = ast.parse(urls_file.read())
        is_api_url_allredy_injected = False
        
        class CheckIsUrlsPatched(ast.NodeTransformer):
            is_api_url_allredy_injected = False
            def visit_Call(self, node):
                if len(node.args) > 0 and node.args[0].s == '^api/v1':
                    self.is_api_url_allredy_injected = True
                return node

        class MainUrlTransformer(ast.NodeTransformer):
            def visit_Assign(self, node):
                if node.targets[0].id == "urlpatterns":
                    api_url_elt = ast.Call(
                        func=ast.Name(id='url', ctx=ast.Load()),
                        args=[ast.Str('^api/v1'), 'include(api_urls.router.urls)'],
                        keywords = [], starargs=None, kwargs=None
                    )
                    api_url_elt.lineno = 5                    
                    node.value.elts.insert(2,api_url_elt)
                return node

        check_is_urls_patched_visitor = CheckIsUrlsPatched()
        check_is_urls_patched_visitor.visit(urls_ast)


        if check_is_urls_patched_visitor.is_api_url_allredy_injected:
            print_warn("  api_urls is already injected to main urls - SKIP")
            return

        urls_ast.body.insert(0, ast.Import(
            names=[
                ast.alias(name='%s.api_urls' % (self.BASE_APP,), asname='api_urls')
            ]
            )
        )

        MainUrlTransformer().visit(urls_ast)
        ast.fix_missing_locations(urls_ast)
        
        urls_file.seek(0)

        out_code = FormatCode(astor.to_source(urls_ast, add_line_information=False))[0]
                
        urls_file.write(out_code)
        urls_file.truncate()
        urls_file.close()
        print_ok("      %s/urls.py - MODIFIED" %(self.BASE_APP, ))

    def init_requirements(self):
        requirements_path = os.path.join(self.BASE_APP,"requirements.txt")
        if os.path.exists(requirements_path):
            return print_warn("  requirements.txt is already exists - SKIP")

        req_file = open(requirements_path, "w")

        req_file.write('Django==%s\n' % (generator_settings.DJANGO_VERSION, ))
        req_file.write('djangorestframework==%s\n' % (generator_settings.DJANGO_REST_FRAMEWORK_VERSION, ) )
        req_file.write("django-filter\n")

        req_file.close()