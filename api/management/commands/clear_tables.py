from django.core.management.base import BaseCommand
from ...model.ator import Atores
from ...model.autoria import Autoria
from ...model.coautoria_edge import CoautoriaEdge
from ...model.coautoria_node import CoautoriaNode
from ...model.comissao import Comissao
from ...model.emenda import Emendas
from ...model.etapa_proposicao import EtapaProposicao
from ...model.info_geral import InfoGerais
from ...model.interesse import Interesse
from ...model.pauta_historico import PautaHistorico
from ...model.pressao import Pressao
from ...model.progresso import Progresso
from ...model.proposicao import Proposicao
from ...model.temperatura_historico import TemperaturaHistorico
from ...model.tramitacao_event import TramitacaoEvent
from ...model.entidade import Entidade
from ...model.autores_proposicao import AutoresProposicao
from ...model.relatores_proposicao import RelatoresProposicao
from ...model.destaques import Destaques
from ...model.governismo import Governismo


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            print("Limpado dados do banco...")
            Atores.objects.all().delete()
            Autoria.objects.all().delete()
            CoautoriaEdge.objects.all().delete()
            CoautoriaNode.objects.all().delete()
            Comissao.objects.all().delete()
            Emendas.objects.all().delete()
            InfoGerais.objects.all().delete()
            PautaHistorico.objects.all().delete()
            Pressao.objects.all().delete()
            Progresso.objects.all().delete()
            TemperaturaHistorico.objects.all().delete()
            TramitacaoEvent.objects.all().delete()
            EtapaProposicao.objects.all().delete()
            Interesse.objects.all().delete()
            Proposicao.objects.all().delete()
            Entidade.objects.all().delete()
            AutoresProposicao.objects.all().delete()
            RelatoresProposicao.objects.all().delete()
            Destaques.objects.all().delete()
            Governismo.objects.all().delete()
        except Exception as e:
            print("Não foi possível limpar os dados do banco =(")
            print(str(e))
