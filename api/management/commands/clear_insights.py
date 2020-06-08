from django.core.management.base import BaseCommand
from ...model.anotacao import Anotacao


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            print("Limpado dados de Insights do banco...")
            Anotacao.objects.all().delete()
        except Exception as e:
            print("Não foi possível limpar os dados de Insights do banco =(")
            print(str(e))
