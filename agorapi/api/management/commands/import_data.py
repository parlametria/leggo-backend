import pandas as pd
from django.core.management.base import BaseCommand
from api.models import Proposicao


class Command(BaseCommand):
    help = 'Importa dados'

    def handle(self, *args, **options):
        df = pd.read_csv('data/proposicoes.csv')
        df.casa = df.casa.apply(lambda r: Proposicao.casas[r])
        Proposicao.objects.bulk_create([
            Proposicao(**r[1].to_dict()) for r in df.iterrows()])
