from django.core.management.base import BaseCommand
from django.conf import settings
from api.utils.csv_servers import (get_token, get_leggo_files)


class Command(BaseCommand):
    help = 'Importa Csvs do servidor remoto'

    def handle(self, *args, **options):
        try:
            print("Obtendo token do servidor remoto...")
            token = get_token(settings.CSVS_SERVER_URL,
                              settings.CSVS_SERVER_USER,
                              settings.CSVS_SERVER_PWD)

            print("Obtendo arquivos csv do servidor remoto...")
            get_leggo_files(settings.CSVS_SERVER_URL, token, settings.CSVS_STORAGE_DIR)

            print("Csvs capturados com sucesso!")
        except Exception as e:
            print("Não foi possível capturar os csvs remotos. =(")
            print(str(e))
