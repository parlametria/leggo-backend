from django.core.management.base import BaseCommand
from django.core import management
import os
import django
import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "agorapi.settings")
django.setup()


class Command(BaseCommand):
    help = 'Importa dados'

    def handle(self, *args, **options):
        try:
            print("----------------------")
            print(datetime.datetime.now())
            print("Apagando Banco de Dados...")
            management.call_command('clear_tables', interactive=False, verbosity=3)
            print("Aplica migrations ao BD...")
            management.call_command('migrate', interactive=False, verbosity=3)
            print("Importando dados a partir de servidor remoto...")
            management.call_command('import_data_from_remote', verbosity=3)
        except Exception as e:
            print("Não foi possível atualizar os dados a partir dos csvs remotos. =(")
            print(str(e))
