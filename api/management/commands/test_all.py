import subprocess

# from django.core.management import call_command
from django.core.management.base import BaseCommand


def pprint(color, text):
    colors = {
        'red': '33',
        'green': '32',
        'white': '37',
    }
    text = f'\n\n{" -"*20}\n{text.center(40)}\n{" -"*20}\n'
    print(f'\033[1;{colors[color]};40m{text}')


class Command(BaseCommand):
    help = 'Roda linter e testes, gerando também análise de cobertura.'

    def handle(self, *args, **options):
        try:
            pprint('white', 'Linter')
            subprocess.run('flake8', check=True)
            pprint('green', 'Ok')
            pprint('white', 'Tests')
            subprocess.run('coverage run ./manage.py test'.split(), check=True)
            pprint('green', 'Ok')
            pprint('white', 'Coverage')
            subprocess.run('coverage report'.split(), check=True)
        except subprocess.CalledProcessError:
            pprint('red', 'Error')
