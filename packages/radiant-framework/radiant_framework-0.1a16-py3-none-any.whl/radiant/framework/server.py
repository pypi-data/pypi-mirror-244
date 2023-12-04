"""
Radiant

"""
import sys
import shutil
import inspect
import traceback

try:
    # Prevent this file to be imported from Brython
    import browser

    sys.exit()
except:
    pass

import os
import json
import jinja2
import pathlib
import importlib.util
from os.path import abspath
from inspect import getsourcefile
from xml.etree import ElementTree
from typing import Union, List, Tuple, Optional

from tornado.web import Application, url, RequestHandler, StaticFileHandler
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer

DEBUG = True
PATH = Union[str, pathlib.Path]
URL = str
DEFAULT_IP = '0.0.0.0'
DEFAULT_PORT = '5000'
DEFAULT_BRYTHON_VERSION = '3.11.2'
DEFAULT_BRYTHON_DEBUG = 0

MAIN = os.path.join(sys.path[0], 'main.py')
if not os.path.exists(MAIN):
    MAIN = sys.argv[0]


########################################################################
class RadiantAPI:
    """Rename Randiant with a new class."""

    # ---------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # ----------------------------------------------------------------------
    def __new__(self):
        """"""
        RadiantServer(self.__name__)


########################################################################
class PythonHandler(RequestHandler):
    def post(self):
        name = self.get_argument('name')
        args = tuple(json.loads(self.get_argument('args')))
        kwargs = json.loads(self.get_argument('kwargs'))

        if v := getattr(self, name, None)(*args, **kwargs):
            if v is None:
                data = json.dumps(
                    {
                        '__RDNT__': 0,
                    }
                )
            else:
                data = json.dumps(
                    {
                        '__RDNT__': v,
                    }
                )
            self.write(data)

    # ----------------------------------------------------------------------
    def test(self):
        """"""
        return True


########################################################################
class JSONHandler(RequestHandler):

    # ----------------------------------------------------------------------
    def initialize(self, **kwargs):
        self.json_data = kwargs

    # ----------------------------------------------------------------------
    def get(self):
        self.write(self.json_data)

    # ----------------------------------------------------------------------
    def test(self):
        """"""
        return True


########################################################################
class ThemeHandler(RequestHandler):

    # ----------------------------------------------------------------------
    def get(self):
        theme = self.get_theme()
        loader = jinja2.FileSystemLoader(
            os.path.join(os.path.dirname(__file__), 'templates')
        )
        env = jinja2.Environment(autoescape=True, loader=loader)
        env.filters['vector'] = self.hex2vector
        stylesheet = env.get_template('theme.css.template')
        self.write(stylesheet.render(**theme))

    # ----------------------------------------------------------------------
    @staticmethod
    def hex2vector(hex_: str):
        return ', '.join([str(int(hex_[i: i + 2], 16)) for i in range(1, 6, 2)])

    # ----------------------------------------------------------------------
    def get_theme(self):
        theme = self.settings['theme']

        if (not theme) or (not os.path.exists(theme)):
            theme = os.path.join(
                os.path.dirname(__file__), 'templates', 'default_theme.xml'
            )

        tree = ElementTree.parse(theme)
        theme_css = {child.attrib['name']: child.text for child in tree.getroot()}
        return theme_css


########################################################################
class RadiantHandler(RequestHandler):

    # ----------------------------------------------------------------------
    def initialize(self, **kwargs):
        self.initial_arguments = kwargs

    # ----------------------------------------------------------------------
    def get(self):
        variables = self.settings.copy()
        variables.update(self.initial_arguments)

        variables['argv'] = json.dumps(variables['argv'])

        if variables['static_app']:
            html = self.render_string(
                f"{os.path.realpath(variables['template'])}", **variables
            )

            parent_dir = f"{variables['class_']}_static"

            if os.path.exists(parent_dir):
                shutil.rmtree(parent_dir)

            shutil.copytree(os.path.dirname(MAIN), os.path.join(parent_dir, 'root'))
            shutil.copytree(os.path.join(os.path.dirname(__file__), 'static'), os.path.join(parent_dir, 'static'))

            with open(os.path.join(parent_dir, 'index.html'), 'wb') as file:
                file.write(html)

            with open(os.path.join(parent_dir, 'environ.json'), 'w') as file:
                json.dump(self.initial_arguments, file)

        self.render(
            f"{os.path.realpath(variables['template'])}", **variables)

    # ----------------------------------------------------------------------
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')


# ----------------------------------------------------------------------
def make_app(
    class_: str,
    /,
    brython_version: str,
    debug_level: int,
    pages: Tuple[str],
    template: PATH = os.path.join(os.path.dirname(
        __file__), 'templates', 'index.html'),
    environ: dict = {},
    mock_imports: Tuple[str] = [],
    handlers: Tuple[URL, Union[List[Union[PATH, str]],
                               RequestHandler], dict] = (),
    python: Tuple[PATH, str] = ([None, None, None]),
    theme: PATH = None,
    path: PATH = None,
    autoreload: bool = False,
    static_app: bool = False,
    templates_path: PATH = None,
    modules: Optional[list] = [],
):
    """
    Parameters
    ----------
    class_ :
        The main class name as string.
    template :
        Path for HTML file with the template.
    environ :
        Dictionary with arguments accessible from the template and main class.
    mock_imports :
        List with modules that exist in Python but not in Brython, this prevents
        imports exceptions.
    handlers :
        Custom handlers for server.
    python :
        Real Python scripting handler.
    theme :
        Path for the XML file with theme colors.
    path :
        Custom directory accesible from Brython PATH.
    autoreload :
        Activate the `autoreload` Tornado feature.
    """

    settings = {
        "debug": DEBUG,
        'static_path': os.path.join(os.path.dirname(__file__), 'static'),
        'static_url_prefix': '/static/',
        "xsrf_cookies": False,
        'autoreload': autoreload,
    }

    if templates_path:
        settings['template_path'] = templates_path

    environ.update(
        {
            'class_': class_,
            # 'python_': python if python else [(None, None)],
            'python_': python,
            'module': os.path.split(sys.path[0])[-1],
            'file': os.path.split(MAIN)[-1].replace('.py', ''),
            'file_path': os.path.join('/root', os.path.split(MAIN)[-1]),
            'theme': theme,
            'argv': [MAIN],
            # 'argv': sys.argv,
            'template': template,
            'mock_imports': mock_imports,
            'path': path,
            'brython_version': brython_version,
            'debug_level': debug_level,
            'static_app': static_app,
            'modules': modules,
        }
    )

    app = []
    if class_:
        app += [url(r'^/$', RadiantHandler, environ)]

    app += [
        url(r'^/theme.css$', ThemeHandler),
        url(r'^/root/(.*)', StaticFileHandler, {'path': sys.path[0]}),
        url(r'^/environ.json$', JSONHandler, environ),
        #url(r'^/manifest.json$', ManifestHandler),
    ]

    if isinstance(pages, str):
        *package, module_name = pages.split('.')
        module = importlib.import_module('.'.join(package))
        pages = getattr(module, module_name)

    for url_, module in pages:
        if '.' in module:
            *file_, class_ = module.split('.')
        else:
            *file_, class_ = f'{os.path.split(MAIN)[-1][:-3]}.{module}'.split('.')

        environ_tmp = environ.copy()
        file_ = '.'.join(file_)
        environ_tmp['file'] = file_
        environ_tmp['class_'] = class_
        app.append(
            url(url_, RadiantHandler, environ_tmp),
        )

    for (module, class_, endpoint) in python:

        if not os.path.isabs(module):
            python_path = os.path.join(sys.path[0], module)
        else:
            python_path = module

        spec = importlib.util.spec_from_file_location(
            '.'.join([module, class_]).replace('.py', ''), python_path
        )
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        app.append(url(f'^{endpoint}', getattr(foo, class_)))

    for handler in handlers:
        if isinstance(handler[1], tuple):
            spec = importlib.util.spec_from_file_location(
                '.'.join(handler[1]).replace('.py', ''),
                os.path.abspath(handler[1][0]),
            )
            foo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(foo)
            app.append(url(handler[0], getattr(
                foo, handler[1][1]), handler[2]))
        else:
            app.append(url(*handler))

    if path:
        app.append(
            url(r'^/path/(.*)', StaticFileHandler, {'path': path}),
        )

    settings.update(environ)

    return Application(app, **settings)


# ----------------------------------------------------------------------
def RadiantServer(
    class_: Optional[str] = None,
    host: str = DEFAULT_IP,
    port: str = DEFAULT_PORT,
    pages: Tuple[str] = (),
    brython_version: str = DEFAULT_BRYTHON_VERSION,
    debug_level: int = DEFAULT_BRYTHON_DEBUG,
    template: PATH = os.path.join(os.path.dirname(
        __file__), 'templates', 'index.html'),
    environ: dict = {},
    mock_imports: Tuple[str] = [],
    handlers: Tuple[URL, Union[List[Union[PATH, str]],
                               RequestHandler], dict] = (),
    python: Tuple[PATH, str] = (),
    theme: Optional[PATH] = None,
    path: Optional[PATH] = None,
    autoreload: Optional[bool] = False,
    callbacks: Optional[tuple] = (),
    static_app: Optional[bool] = False,
    templates_path: PATH = None,
    modules: Optional[list] = [],
    **kwargs,
):
    """Python implementation for move `class_` into a Bython environment.

    Configure the Tornado server and the Brython environment for run the
    `class_` in both frameworks at the same time.

    Parameters
    ----------
    class_ :
        The main class name as string.
    host :
        The host for server.
    port :
        The port for server.
    template :
        Path for HTML file with the template.
    environ :
        Dictionary with arguments accessible from the template and main class.
    mock_imports :
        List with modules that exist in Python but not in Brython, this prevents
        imports exceptions.
    handlers :
        Custom handlers for server.
    python :
        Real Python scripting handler.
    theme :
        Path for the XML file with theme colors.
    path :
        Custom directory accesible from Brython PATH.
    autoreload :
        Activate the `autoreload` Tornado feature.

    """

    print("Radiant server running on port {}".format(port))
    application = make_app(
        class_,
        python=python,
        template=template,
        handlers=handlers,
        theme=theme,
        environ=environ,
        mock_imports=mock_imports,
        path=path,
        brython_version=brython_version,
        pages=pages,
        debug_level=debug_level,
        static_app=static_app,
        templates_path=templates_path,
        modules=modules,
    )
    http_server = HTTPServer(
        application,
    )
    http_server.listen(port, host)

    for handler in callbacks:
        if isinstance(handler, tuple):
            spec = importlib.util.spec_from_file_location(
                '.'.join(handler).replace('.py', ''),
                os.path.abspath(handler[0]),
            )
            foo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(foo)
            getattr(foo, handler[1])()
        else:
            handler()

    IOLoop.instance().start()


# ----------------------------------------------------------------------
def render(*args, **kwargs):
    """"""
    return None

