from django.core.management.base import BaseCommand
from django_materialize.management.secret_key import secret_key


class Command(BaseCommand):
    help = 'Generate a secret key'

    def add_arguments(self, parser):
        parser.add_argument('size', default=50, type=int)

    def handle(self, *args, **options):
        self.stdout.write(secret_key(options['size']))
