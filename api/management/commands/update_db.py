from django.core.management.base import BaseCommand
import subprocess


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Command(BaseCommand):
    help = 'Atualiza banco de dados.'

    def handle(self, *args, **options):
        try:
            print(bcolors.OKBLUE + 'Gerando migracoes...' + bcolors.ENDC)
            subprocess.run('./manage.py makemigrations'.split(), check=True)

            print(bcolors.OKBLUE, 'Migrando banco de dados...' + bcolors.ENDC)
            subprocess.run('./manage.py migrate'.split(), check=True)

            print(bcolors.OKBLUE, 'Apaga dados antigos...' + bcolors.ENDC)
            subprocess.run('./manage.py flush --no-input'.split(), check=True)

            print(bcolors.OKBLUE, 'Importando dados novos...' + bcolors.ENDC)
            subprocess.run('./manage.py import_all_data'.split(), check=True)

        except subprocess.CalledProcessError:
            print(bcolors.FAIL, 'OCORREU UM ERRO')
            exit(1)
