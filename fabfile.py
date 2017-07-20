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


###############################################################################
# Tasks
###############################################################################

@task
def manage(*args, **kwargs):
    production = _prep_bool_arg(kwargs.get('production', True))
    django_settings_module = 'django_materialize.settings' if production else 'django_materialize.settings.development'

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
