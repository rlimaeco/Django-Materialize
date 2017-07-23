import os

from contextlib import contextmanager as _contextmanager
from distutils.util import strtobool
from fabric.api import local, cd
from fabric.context_managers import prefix, shell_env
from fabric.decorators import task


PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))
VIRTUALENV_PATH = os.path.join(PROJECT_PATH, 'venv')
PYTHON_PATH = '/usr/bin/python3.6'
SUPERVISOR_PATH = '/etc/supervisor/conf.d'


@_contextmanager
def virtualenv():
    with cd(PROJECT_PATH):
        with prefix('. {0}/bin/activate'.format(VIRTUALENV_PATH)):
            yield


def _prep_bool_arg(arg):
    return bool(strtobool(str(arg)))


def create_virtualenv():
    local('virtualenv -p {0} venv'.format(PYTHON_PATH))


def get_scss_files():
    matches = []
    for root, dir_names, file_names in os.walk('src'):
        for file_name in file_names:
            if not file_name.startswith("_") and file_name.endswith(".scss"):
                matches.append(os.path.join(root, file_name))
    return matches


###############################################################################
# Tasks
###############################################################################
@task
def convert_from_scss_to_css():
    scss_files = get_scss_files()

    for scss_file in scss_files:
        scss_directory = os.path.dirname(scss_file)
        css_directory = os.path.join(scss_directory, "..", "css")

        if not os.path.exists(css_directory):
            os.makedirs(css_directory)

        filename = os.path.basename(scss_file)
        filename_without_extension = os.path.splitext(filename)[0]
        css_file = "{path}.css".format(
            path=os.path.join(css_directory, filename_without_extension)
        )
        local('sass {scss_file}:{css_file} --style compressed'.format(
            scss_file=scss_file, css_file=css_file)
        )


@task
def manage(*args, **kwargs):
    production = _prep_bool_arg(kwargs.get('production', True))
    django_settings_module = '{{ project_name }}.settings' if production else '{{ project_name }}.settings.development'

    with cd(PROJECT_PATH), virtualenv(), shell_env(DJANGO_SETTINGS_MODULE=django_settings_module):
        local('./src/manage.py %s' % ' '.join(args))


@task
def deploy(production=True, start_app=False):
    production = _prep_bool_arg(production)
    start_app = _prep_bool_arg(start_app)

    create_virtualenv()
    with virtualenv():
        if production:
            local('pip install -r ./requirements/production.txt')
        else:
            local('pip install -r ./requirements/development.txt')
    convert_from_scss_to_css()
    manage("migrate", production=production)
    manage("test", production=production)
    if production:
        manage("collectstatic", production=production)
    if start_app:
        runserver(production=production)


@task
def runserver(production=True):
    production = _prep_bool_arg(production)

    if production:
        # TODO
        pass
    else:
        manage("runserver", production=production)


@task
def test(coverage=True):
    coverage = _prep_bool_arg(coverage)

    if coverage:
        with virtualenv():
            local("coverage run --source='.' src/manage.py test")
            local('coverage report')
    else:
        manage("test", production=False)
