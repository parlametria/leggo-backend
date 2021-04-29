from api.management.commands.import_utils import (
    import_entidades,
    import_etapas_proposicoes,
    import_proposicoes,
    import_interesse,
    import_tramitacoes,
    import_temperaturas,
    import_progresso,
    import_pautas,
    import_emendas,
    import_comissoes,
    import_atores,
    import_pressao,
    import_coautoria_node,
    import_coautoria_edge,
    import_autoria,
    import_autores_proposicoes,
    import_relatores_proposicoes,
    import_destaques,
    import_governismo,
    import_disciplina,
    import_votacoes_sumarizadas,
    import_locais_atuais_proposicoes,
    import_proposicoes_apensadas,
    import_anotacoes_especificas
)

from ...model.ator import Atores
from ...model.autoria import Autoria
from ...model.coautoria_edge import CoautoriaEdge
from ...model.coautoria_node import CoautoriaNode
from ...model.comissao import Comissao
from ...model.emenda import Emendas
from ...model.etapa_proposicao import EtapaProposicao
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
from ...model.disciplina import Disciplina
from ...model.votacoes_sumarizadas import VotacoesSumarizadas
from ...model.local_atual_proposicao import LocalAtualProposicao
from ...model.proposicao_apensada import ProposicaoApensada
from ...model.anotacao import Anotacao


def atualiza_atores():
    Atores.objects.all().delete()
    import_atores()


def atualiza_autorias():
    Autoria.objects.all().delete()
    import_autoria()


def atualiza_coautoria_edge():
    CoautoriaEdge.objects.all().delete()
    import_coautoria_edge()


def atualiza_coautoria_node():
    CoautoriaNode.objects.all().delete()
    import_coautoria_node()


def atualiza_comissoes():
    Comissao.objects.all().delete()
    import_comissoes()


def atualiza_emendas():
    Emendas.objects.all().delete()
    import_emendas()


def atualiza_pauta():
    PautaHistorico.objects.all().delete()
    import_pautas()


def atualiza_pressao():
    Pressao.objects.all().delete()
    import_pressao()


def atualiza_progresso():
    Progresso.objects.all().delete()
    import_progresso()


def atualiza_temperatura():
    TemperaturaHistorico.objects.all().delete()
    import_temperaturas()


def atualiza_tramitacoes():
    TramitacaoEvent.objects().all().delete()
    import_tramitacoes()


def atualiza_interesse():
    Interesse.objects.all().delete()
    import_interesse()
    atualiza_pressao()


def atualiza_autores_proposicoes():
    AutoresProposicao.objects.all().delete()
    import_autores_proposicoes()


def atualiza_relatores_proposicoes():
    RelatoresProposicao.objects.all().delete()
    import_relatores_proposicoes()


def atualiza_destaque():
    Destaques.objects.all().delete()
    import_destaques()


def atualiza_governismo():
    Governismo.objects.all().delete()
    import_governismo()


def atualiza_disciplina():
    Disciplina.objects.all().delete()
    import_disciplina()


def atualiza_votacoes_sumarizadas():
    VotacoesSumarizadas.objects.all().delete()
    import_votacoes_sumarizadas()


def atualiza_locais_atuais():
    LocalAtualProposicao.objects.all().delete()
    import_locais_atuais_proposicoes()


def atualiza_proposicoes_apensadas():
    ProposicaoApensada.objects.all().delete()
    import_proposicoes_apensadas()


def atualiza_anotacoes_especificas():
    Anotacao.objects.all().delete()
    import_anotacoes_especificas()


def atualiza_entidades():
    Entidade.objects.all().delete()

    import_entidades()
    atualiza_etapa_proposicao()
    atualiza_governismo()
    atualiza_disciplina()
    atualiza_votacoes_sumarizadas()


def atualiza_etapa_proposicao():
    EtapaProposicao.objects.all().delete()

    import_etapas_proposicoes()
    atualiza_proposicoes()
    atualiza_tramitacoes()
    atualiza_autorias()
    atualiza_pauta()
    atualiza_progresso()
    atualiza_emendas()


def atualiza_proposicoes():
    Proposicao.objects.all().delete()

    import_proposicoes()
    atualiza_interesse()
    atualiza_temperatura()
    atualiza_coautoria_node()
    atualiza_coautoria_edge()
    atualiza_atores()
    atualiza_anotacoes_especificas()
    atualiza_autores_proposicoes()
    atualiza_relatores_proposicoes()
    atualiza_destaque()
    atualiza_locais_atuais()
    atualiza_proposicoes_apensadas()


def get_models():
    return [
      "ator",
      "comissao",
      "emenda",
      "etapa_proposicao",
      "pauta_historico",
      "pressao",
      "progresso",
      "proposicao",
      "temperatura_historico",
      "tramitacao_event",
      "coautoria_node",
      "coautoria_edge",
      "autoria",
      "interesse",
      "entidade",
      "autores_proposicao",
      "relatores_proposicao",
      "destaques",
      "governismo",
      "disciplina",
      "votacoes_sumarizadas",
      "local_atual_proposicao",
      "proposicao_apensada"
    ]
