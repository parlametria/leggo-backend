from django.core.management.base import BaseCommand
from django.conf import settings
from api.utils.csv_servers import (get_token, get_leggo_files)
from .import_utils import import_all_data


class Command(BaseCommand):
    help = 'Importa dados'

    def handle(self, *args, **options):
        try:
            print("Apagando Banco de Dados...")
            management.call_command('flush', interactive=False)
            print("Importando dados a partir de servidor remoto...")
            management.call_command('import_data_from_remote', verbosity=3)
        except Exception as e:
            print("Não foi possível atualizar os dados a partir dos csvs remotos. =(")
            print(str(e))
