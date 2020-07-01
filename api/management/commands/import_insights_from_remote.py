from django.core.management.base import BaseCommand
from django.conf import settings
from api.utils.csv_servers import get_token, get_file
from .import_utils import import_insights


class Command(BaseCommand):
    help = "Importa dados"

    def handle(self, *args, **options):
        try:
            print("Obtendo token do servidor remoto...")
            token = get_token(
                settings.CSVS_SERVER_URL,
                settings.CSVS_SERVER_USER,
                settings.CSVS_SERVER_PWD,
            )

            print("Obtendo arquivos csv do servidor remoto...")
            get_file(
                settings.CSVS_SERVER_URL,
                token,
                "anotacoes_especificas.csv",
                settings.CSVS_STORAGE_DIR,
            )

            get_file(
                settings.CSVS_SERVER_URL,
                token,
                "anotacoes_gerais.csv",
                settings.CSVS_STORAGE_DIR,
            )

            print("Inserindo novos dados no BD...")
            import_insights()

            print("Dados de insights atualizados com sucesso!")
        except Exception as e:
            print("Não foi possível atualizar os dados a partir dos csvs remotos. =(")
            print(str(e))
