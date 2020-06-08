from django.core.management.base import BaseCommand
from .import_utils import import_all_data


class Command(BaseCommand):
    help = "Importa dados"

    def handle(self, *args, **options):
        import_all_data()
