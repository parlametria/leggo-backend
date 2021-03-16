import os
import datetime
import pandas as pd
import numpy as np
from api.model.ator import Atores
from api.model.comissao import Comissao
from api.model.emenda import Emendas
from api.model.etapa_proposicao import EtapaProposicao
from api.model.info_geral import InfoGerais
from api.model.pauta_historico import PautaHistorico
from api.model.pressao import Pressao
from api.model.progresso import Progresso
from api.model.proposicao import Proposicao
from api.model.temperatura_historico import TemperaturaHistorico
from api.model.tramitacao_event import TramitacaoEvent
from api.model.coautoria_node import CoautoriaNode
from api.model.coautoria_edge import CoautoriaEdge
from api.model.autoria import Autoria
from api.model.interesse import Interesse
from api.model.anotacao import Anotacao
from api.model.anotacao_geral import AnotacaoGeral
from api.model.entidade import Entidade
from api.model.autores_proposicao import AutoresProposicao
from api.model.relatores_proposicao import RelatoresProposicao
from api.model.destaques import Destaques
from api.model.votacao import Votacao
from api.model.voto import Voto
from api.model.governismo import Governismo
from api.model.disciplina import Disciplina
from api.utils.relator import check_relator_id
from api.utils.sigla import cria_sigla


def print_import_info(table):
    print('\n============================================================')
    print(f'Importando os dados de {table}')
    print('==============================================================')


def import_etapas_proposicoes():
    """Carrega etapas das proposições"""

    print_import_info("Etapas proposições")

    props_df = pd.read_csv("data/proposicoes.csv", decimal=",").assign(
        data_apresentacao=lambda x: x.data_apresentacao.apply(lambda s: s.split("T")[0])
    )

    props_df.casa = props_df.casa.apply(lambda r: EtapaProposicao.casas[r])
    props_df = props_df.fillna(-1)

    props_df = props_df.groupby(["id_leggo", "relator_id_parlametria"])

    for group_index in props_df.groups:
        relator = None

        # Pesquisa a entidade somente se o relator_id_parlametria
        # for diferente de NaN (representado por -1)
        if group_index[1] != -1:

            id_entidade_parlametria = {"id_entidade_parlametria": group_index[1]}

            relator = get_entidade(id_entidade_parlametria, "EtapaProposicao")

        group_df = (
            props_df.get_group(group_index)
            .assign(relatoria=relator)
            .replace(-1, np.nan)
        )

        array = []
        for r in group_df.iterrows():
            r[1]["relator_id"] = check_relator_id(r[1]["relator_id"])
            r[1]["relator_id_parlametria"] = check_relator_id(
                r[1]["relator_id_parlametria"]
            )
            array.append(EtapaProposicao(**r[1].to_dict()))

        EtapaProposicao.objects.bulk_create(array)


def import_proposicoes():
    """Carrega proposições"""

    print_import_info("Proposições")

    props_df = pd.read_csv("data/proposicoes.csv")

    for _, etapas_df in props_df.groupby(["id_leggo"]):
        etapas = []
        sigla_camara = ''
        sigla_senado = ''
        for _, etapa in etapas_df.iterrows():
            etapas.append(
                EtapaProposicao.objects.get(casa=etapa.casa, id_ext=etapa.id_ext)
            )
        prop = Proposicao(id_leggo=etapa.id_leggo)
        prop.save()

        # formata siglas
        if len(etapas) == 2:
            if etapas[0].casa == 'camara':
                sigla_camara = cria_sigla(etapas[0])
                sigla_senado = cria_sigla(etapas[1])

            elif etapas[0].casa == 'senado':
                sigla_senado = cria_sigla(etapas[0])
                sigla_camara = cria_sigla(etapas[1])

            prop.sigla_camara = sigla_camara
            prop.save()
            prop.sigla_senado = sigla_senado
            prop.save()

        else:
            if etapas[0].casa == 'camara':
                sigla_camara = cria_sigla(etapas[0])
                prop.sigla_camara = sigla_camara
                prop.save()

            elif etapas[0].casa == 'senado':
                sigla_senado = cria_sigla(etapas[0])
                prop.sigla_senado = sigla_senado
                prop.save()

        prop.etapas.set(etapas)
        prop.save()


def import_tramitacoes():
    """Carrega tramitações"""

    print_import_info("Tramitações")

    filepath = "data/trams.csv"
    col_dtypes = {
        'data': str,
        'evento': str,
        'titulo_evento': str,
        'sigla_local': str,
        'local': str,
        'descricao_situacao': str,
        'texto_tramitacao': str,
        'status': str,
        'tipo_documento': str,
        'link_inteiro_teor': str
    }

    col_names = [
        "data",
        "casa",
        "id_ext",
        "sequencia",
        "evento",
        "titulo_evento",
        "sigla_local",
        "local",
        "nivel",
        "temperatura_local",
        "temperatura_evento",
        "descricao_situacao",
        "texto_tramitacao",
        "status",
        "tipo_documento",
        "link_inteiro_teor"
    ]

    grouped = (
        pd.read_csv(filepath, usecols=col_names, dtype=col_dtypes)
        .rename(columns={'descricao_situacao': 'situacao'})
        .groupby(["casa", "id_ext"])
    )

    for group_index in grouped.groups:
        prop_id = {
            "casa": group_index[0],
            "id_ext": group_index[1],
        }

        etapa_prop = get_etapa_proposicao(prop_id, "Eventos da Tramitação")

        if etapa_prop is None:
            continue

        group_df = (
            grouped.get_group(group_index)
            .drop(['id_ext', 'casa'], axis=1)
            # pega apenas a data e não a hora
            .assign(data=lambda x: x.data.apply(lambda s: s.split("T")[0]))
            # eventos sem nível recebem o maior valor (ou seja, são menos importantes)
            .assign(nivel=lambda x: x.nivel.fillna(x.nivel.max()))
            .assign(etapa_proposicao=etapa_prop)
        )
        TramitacaoEvent.objects.bulk_create(
            TramitacaoEvent(**r[1].to_dict()) for r in group_df.iterrows()
        )

    last_update = datetime.datetime.utcfromtimestamp(os.path.getmtime(filepath))
    InfoGerais.objects.create(name="last_update_trams", value=last_update.isoformat())


def import_temperaturas():
    """Carrega históricos de temperatura"""

    print_import_info("Histórico de temperatura")

    grouped = pd.read_csv("data/hists_temperatura.csv").groupby(["id_leggo"])
    for group_index in grouped.groups:
        id_leggo = {"id_leggo": group_index}

        prop = get_proposicao(id_leggo, "Histórico de Temperatura")

        if prop is None:
            continue

        group_df = (
            grouped.get_group(group_index)
            .assign(periodo=lambda x: x.periodo.apply(lambda s: s.split("T")[0]))
            .filter(["periodo", "temperatura_periodo", "temperatura_recente"])
            .assign(proposicao=prop)
        )
        TemperaturaHistorico.objects.bulk_create(
            TemperaturaHistorico(**r[1].to_dict()) for r in group_df.iterrows()
        )


def import_coautoria_node():
    """Carrega nós"""

    print_import_info("Nós de coautorias")

    grouped = pd.read_csv("data/coautorias_nodes.csv").groupby(["id_leggo"])
    for group_index in grouped.groups:
        id_leggo = {"id_leggo": group_index}

        prop = get_proposicao(id_leggo, "Coautorias Nodes")

        if prop is None:
            continue

        group_df = grouped.get_group(group_index)
        CoautoriaNode.objects.bulk_create(
            CoautoriaNode(**r[1].to_dict()) for r in group_df.iterrows()
        )


def import_coautoria_edge():
    """Carrega arestas"""

    print_import_info("Arestas de coautorias")

    grouped = pd.read_csv("data/coautorias_edges.csv").groupby(["id_leggo"])
    for group_index in grouped.groups:
        id_leggo = {"id_leggo": group_index}

        prop = get_proposicao(id_leggo, "Coautorias Edges")

        if prop is None:
            continue

        group_df = grouped.get_group(group_index)
        CoautoriaEdge.objects.bulk_create(
            CoautoriaEdge(**r[1].to_dict()) for r in group_df.iterrows()
        )


def import_autoria():
    """Carrega autorias"""

    print_import_info("Autorias")

    grouped = pd.read_csv(
        "data/autorias.csv").groupby(["casa", "id_principal", "id_autor_parlametria"])
    for group_index in grouped.groups:
        prop_id = {
            "casa": group_index[0],
            "id_ext": group_index[1],
        }
        etapa_prop = get_etapa_proposicao(prop_id, "Autorias")

        id_entidade_parlametria = {"id_entidade_parlametria": group_index[2]}
        entidade_relacionada = get_entidade(
            id_entidade_parlametria, "AutoriasroposicaoEntidade"
        )

        if etapa_prop is None:
            continue

        if entidade_relacionada is None:
            continue

        group_df = (
            grouped.get_group(group_index)
            # pega apenas a data e não a hora
            .assign(data=lambda x: x.data.apply(lambda s: s.split("T")[0]))
            .assign(
                etapa_proposicao=etapa_prop
            )
            .assign(entidade=entidade_relacionada)
        )
        Autoria.objects.bulk_create(
            Autoria(**r[1].to_dict()) for r in group_df.iterrows()
        )


def import_pautas():
    """Carrega históricos de pautas"""

    print_import_info("Histórico de pautas")

    grouped = pd.read_csv("data/pautas.csv").groupby(["casa", "id_ext"])
    for group_index in grouped.groups:
        prop_id = {
            "casa": group_index[0],
            "id_ext": group_index[1],
        }

        etapa_prop = get_etapa_proposicao(prop_id, "Pautas")

        if etapa_prop is None:
            continue

        group_df = (
            grouped.get_group(group_index)
            .assign(proposicao=etapa_prop)
            .filter(["data", "semana", "local", "em_pauta", "proposicao"])
        )
        PautaHistorico.objects.bulk_create(
            PautaHistorico(**r[1].to_dict()) for r in group_df.iterrows()
        )


def import_progresso():
    """Carrega o progresso das proposições"""

    print_import_info("Progressos")

    progresso_df = pd.read_csv("data/progressos.csv")

    for col in ["data_inicio", "data_fim"]:
        progresso_df[col] = (
            progresso_df[col]
            .astype("str")
            .apply(
                lambda x: None
                if x == "NA"
                else pd.to_datetime(x.split("T")[0], format="%Y-%m-%d")
            )
        )

    grouped = progresso_df.groupby(["casa", "id_ext"])

    for group_index in grouped.groups:
        if any(map(pd.isna, group_index)):
            print("Aviso: dados de progresso possuem NAN nos identificadores!")
            continue
        prop_id = {
            "casa": group_index[0],
            "id_ext": group_index[1],
        }

        etapa_prop = get_etapa_proposicao(prop_id, "Progresso")

        if etapa_prop is None:
            continue

        group_df = (
            grouped.get_group(group_index)
            .filter(
                [
                    "data_inicio",
                    "data_fim",
                    "local",
                    "fase_global",
                    "local_casa",
                    "pulou",
                ]
            )
            .assign(proposicao=etapa_prop.proposicao)
            .assign(data_inicio=lambda x: x.data_inicio.astype("object"))
            .assign(data_fim=lambda x: x.data_fim.astype("object"))
        )
        Progresso.objects.bulk_create(
            Progresso(**r[1].to_dict())
            for r in group_df.where(pd.notnull(group_df), None).iterrows()
        )


def import_emendas():
    """Carrega emendas"""

    print_import_info("Emendas")

    emendas_df = pd.read_csv("data/emendas.csv").groupby(["casa", "id_ext"])
    for group_index in emendas_df.groups:
        prop_id = {
            "casa": group_index[0],
            "id_ext": group_index[1],
        }

        etapa_prop = get_etapa_proposicao(prop_id, "Emendas")

        if etapa_prop is None:
            continue

        group_df = emendas_df.get_group(group_index)[
            [
                "codigo_emenda",
                "numero",
                "distancia",
                "tipo_documento",
                "data_apresentacao",
                "local",
                "autor",
                "inteiro_teor",
            ]
        ].assign(proposicao=etapa_prop)
        Emendas.objects.bulk_create(
            Emendas(**r[1].to_dict()) for r in group_df.iterrows()
        )


def import_atores():
    """Carrega Atores"""

    print_import_info("Atores")

    atores_df = pd.read_csv("data/atuacao.csv").groupby(
        ["id_leggo", "id_autor_parlametria"]
    )

    for group_index in atores_df.groups:

        id_entidade_parlametria = {"id_entidade_parlametria": group_index[1]}

        id_leggo = {"id_leggo": group_index[0]}

        prop = get_proposicao(id_leggo, "Atores")
        entidade_relacionada = get_entidade(
            id_entidade_parlametria, "AtoresProposicaoEntidade"
        )

        if entidade_relacionada is None:
            continue

        if prop is None:
            continue

        group_df = (
            atores_df.get_group(group_index)[
                [
                    "id_leggo",
                    "id_ext",
                    "casa",
                    "id_autor",
                    "peso_total_documentos",
                    "num_documentos",
                    "tipo_generico",
                    "tipo_acao",
                    "sigla_local",
                    "is_important",
                    "bancada",
                    "id_autor_parlametria",
                    "casa_autor",
                ]
            ]
            .assign(proposicao=prop)
            .assign(entidade=entidade_relacionada)
        )
        Atores.objects.bulk_create(
            Atores(**r[1].to_dict()) for r in group_df.iterrows()
        )


def import_comissoes():
    """Carrega Comissoes"""

    print_import_info("Comissões")

    comissoes_df = pd.read_csv("data/comissoes.csv").groupby(["casa", "sigla"])
    for group_index in comissoes_df.groups:
        group_df = comissoes_df.get_group(group_index)
        Comissao.objects.bulk_create(
            Comissao(**r[1].to_dict()) for r in group_df.iterrows()
        )


def import_pressao():
    """Carrega pressao das proposicoes"""

    print_import_info("Pressão")

    pressao_df = pd.read_csv("data/pressao.csv").groupby(
        ["id_leggo", "id_ext", "casa", "interesse", "date"]
    )
    for group_index in pressao_df.groups:

        id_leggo = {"id_leggo": group_index[0]}

        interesse_obj = {"id_leggo": group_index[0], "interesse": group_index[3]}

        prop = get_proposicao(id_leggo, "Pressão")
        inter = get_interesse(interesse_obj, "Pressão Interesse")

        if prop is None:
            continue

        if inter is None:
            continue

        group_df = (
            pressao_df.get_group(group_index)[
                [
                    "id_leggo",
                    "id_ext",
                    "casa",
                    "interesse",
                    "date",
                    "trends_max_pressao_principal",
                    "trends_max_pressao_rel",
                    "trends_max_popularity",
                    "twitter_mean_popularity",
                    "popularity",
                ]
            ]
            .assign(proposicao=prop)
            .assign(interesse_relacionado=inter)
        )

        Pressao.objects.bulk_create(
            Pressao(**r[1].to_dict()) for r in group_df.iterrows()
        )


def get_etapa_proposicao(prop_id, entity_str):
    etapa_prop = None

    try:
        etapa_prop = EtapaProposicao.objects.get(**prop_id)
    except Exception as e:
        print("Não foi possivel encontrar a etapa proposição: {}".format(str(prop_id)))
        print("\tErro ao inserir: {}".format(str(entity_str)))
        print("\t{}".format(str(e)))

    return etapa_prop


def get_proposicao(leggo_id, entity_str):
    prop = None

    if pd.isna(leggo_id['id_leggo']):
        return prop

    try:
        prop = Proposicao.objects.get(**leggo_id)
    except Exception as e:
        print("Não foi possivel encontrar a proposição: {}".format(str(leggo_id)))
        print("\tErro ao inserir: {}".format(str(entity_str)))
        print("\t{}".format(str(e)))

    return prop


def get_interesse(interesse_obj, entity_str):
    interesse = None

    try:
        interesse = Interesse.objects.get(**interesse_obj)
    except Exception as e:
        print("Não foi possivel encontrar o interesse: {}".format(str(interesse_obj)))
        print("\tErro ao inserir: {}".format(str(entity_str)))
        print("\t{}".format(str(e)))

    return interesse


def get_entidade(entidade_obj, entity_str):
    entidade = None

    try:
        entidade = (
            Entidade.objects.filter(**entidade_obj)
            .order_by("id_entidade_parlametria", "-legislatura")
            .distinct("id_entidade_parlametria")
            .first()
        )
    except Exception as e:
        print("Não foi possivel encontrar a entidade: {}".format(str(entidade_obj)))
        print("\tErro ao inserir: {}".format(str(entity_str)))
        print("\t{}".format(str(e)))

    return entidade


def import_interesse():
    """Carrega Interesses"""

    print_import_info("Interesses")

    grouped = pd.read_csv("data/interesses.csv").groupby(["id_leggo"])
    for group_index in grouped.groups:
        id_leggo = {"id_leggo": group_index}

        prop = get_proposicao(id_leggo, "Interesse")

        if prop is None:
            continue

        group_df = grouped.get_group(group_index)[
            [
                "id_leggo",
                "interesse",
                "nome_interesse",
                "descricao_interesse",
                "apelido",
                "keywords",
                "tema",
                "tema_slug",
                "advocacy_link",
                "tipo_agenda",
            ]
        ].assign(proposicao=prop)
        Interesse.objects.bulk_create(
            Interesse(**r[1].to_dict()) for r in group_df.iterrows()
        )


def import_anotacoes_especificas():
    """Carrega anotações das proposições"""

    print_import_info("Anotações específicas")

    grouped = pd.read_csv("data/anotacoes_especificas.csv").groupby(["id_leggo"])

    for group_index in grouped.groups:
        id_leggo = {"id_leggo": group_index}

        prop = get_proposicao(id_leggo, "Anotação")

        if prop is None:
            continue

        group_df = grouped.get_group(group_index)[
            [
                "id_leggo",
                "data_criacao",
                "data_ultima_modificacao",
                "autor",
                "categoria",
                "titulo",
                "anotacao",
                "peso",
                "interesse",
            ]
        ].assign(proposicao=prop)
        Anotacao.objects.bulk_create(
            Anotacao(**r[1].to_dict()) for r in group_df.iterrows()
        )


def import_anotacoes_gerais():
    """Carrega anotações dos interesses"""

    print_import_info("Anotações gerais")

    anotacoes = pd.read_csv("data/anotacoes_gerais.csv")

    AnotacaoGeral.objects.bulk_create(
        AnotacaoGeral(**r[1].to_dict()) for r in anotacoes.iterrows()
    )


def import_entidades():

    print_import_info("Entidades")

    grouped = pd.read_csv("data/entidades.csv")

    grouped = grouped.groupby(["legislatura", "id_entidade_parlametria"])

    for group_index in grouped.groups:

        group_df = grouped.get_group(group_index)[
            [
                "legislatura",
                "id_entidade",
                "id_entidade_parlametria",
                "casa",
                "nome",
                "sexo",
                "partido",
                "uf",
                "situacao",
                "em_exercicio",
                "is_parlamentar",
            ]
        ]

        Entidade.objects.bulk_create(
            Entidade(**r[1].to_dict()) for r in group_df.iterrows()
        )


def import_autores_proposicoes():
    """Carrega Autores das proposições"""

    print_import_info("Autores de proposições")

    grouped = pd.read_csv("data/autores_leggo.csv")
    grouped = grouped.groupby(["id_autor_parlametria", "id_leggo"])

    for group_index in grouped.groups:
        id_entidade_parlametria = {"id_entidade_parlametria": group_index[0]}

        id_leggo = {"id_leggo": group_index[1]}

        entidade_relacionada = get_entidade(
            id_entidade_parlametria, "AutoresProposicaoEntidade"
        )

        prop = get_proposicao(id_leggo, "AutoresProposicaoProp")

        if entidade_relacionada is None:
            continue

        if prop is None:
            continue

        group_df = (
            grouped.get_group(group_index)[
                [
                    "id_leggo",
                    "id_camara",
                    "id_senado",
                    "id_autor_parlametria",
                    "id_autor",
                ]
            ]
            .assign(entidade=entidade_relacionada)
            .assign(proposicao=prop)
        )

        a = []
        for r in group_df.iterrows():
            if r[1]["id_camara"] == "None":
                r[1]["id_camara"] = None

            if r[1]["id_senado"] == "None":
                r[1]["id_senado"] = None

            a.append(AutoresProposicao(**r[1].to_dict()))

        AutoresProposicao.objects.bulk_create(a)


def import_relatores_proposicoes():
    """Carrega Relatores das proposições"""

    print_import_info("Relatores")

    grouped = pd.read_csv("data/relatores_leggo.csv")
    grouped = grouped.groupby(["relator_id_parlametria", "id_leggo"])

    for group_index in grouped.groups:
        id_entidade_parlametria = {"id_entidade_parlametria": group_index[0]}

        id_leggo = {"id_leggo": group_index[1]}

        entidade_relacionada = get_entidade(
            id_entidade_parlametria, "RelatoresProposicaoEntidade"
        )

        prop = get_proposicao(id_leggo, "RelatoresroposicaoProp")

        if entidade_relacionada is None:
            continue

        if prop is None:
            continue

        group_df = (
            grouped.get_group(group_index)[
                [
                    "id_leggo",
                    "id_ext",
                    "casa",
                    "relator_id",
                    "relator_id_parlametria",
                    "relator_nome",
                ]
            ]
            .assign(entidade=entidade_relacionada)
            .assign(proposicao=prop)
        )

        a = []
        for r in group_df.iterrows():
            if r[1]["id_ext"] == "NA":
                r[1]["id_camara"] = None

            r[1]["relator_id"] = check_relator_id(r[1]["relator_id"])
            r[1]["relator_id_parlametria"] = check_relator_id(
                r[1]["relator_id_parlametria"]
            )

            a.append(RelatoresProposicao(**r[1].to_dict()))

        RelatoresProposicao.objects.bulk_create(a)


def import_destaques():
    """Carrega proposições em destaques"""

    print_import_info("Destaques")

    destaques_df = pd.read_csv("data/proposicoes_destaques.csv")

    for col in ["data_aprovacao", "data_req_urgencia_apresentado",
                "data_req_urgencia_aprovado"]:
        destaques_df[col] = (
            destaques_df[col]
            .astype("str")
            .apply(
                lambda x: None
                if x == "NA"
                else pd.to_datetime(x)
            )
        )

    grouped = destaques_df.groupby(["id_leggo"])

    for group_index in grouped.groups:
        id_leggo = {"id_leggo": group_index}

        prop = get_proposicao(id_leggo, "Destaques")
        group_df = (
            grouped.get_group(group_index)
            .assign(data_aprovacao=lambda x: x.data_aprovacao.astype("object"))
            .assign(
                data_req_urgencia_apresentado=(
                    lambda x: x.data_req_urgencia_apresentado.astype("object"))
            )
            .assign(
                data_req_urgencia_aprovado=(
                    lambda x: x.data_req_urgencia_aprovado.astype("object"))
            )
            .assign(proposicao=prop)
        )
        Destaques.objects.bulk_create(
            Destaques(**r[1].to_dict())
            for r in group_df.where(pd.notnull(group_df), None).iterrows()
        )


def import_governismo():
    """Carrega dados de governismo"""

    print_import_info("Governismo")

    governismo_df = pd.read_csv("data/governismo.csv")

    grouped = governismo_df.groupby(["id_parlamentar_parlametria"])

    for group_index in grouped.groups:
        id_entidade_parlametria = {"id_entidade_parlametria": group_index}

        entidade_relacionada = get_entidade(
            id_entidade_parlametria, "GovernismoEntidade"
        )

        if entidade_relacionada is None:
            continue

        group_df = (
            grouped.get_group(group_index)[
                [
                    "id_parlamentar",
                    "id_parlamentar_parlametria",
                    "casa",
                    "governismo"
                ]
            ]
            .assign(entidade=entidade_relacionada)
        )

        Governismo.objects.bulk_create(
            Governismo(**r[1].to_dict())
            for r in group_df.where(pd.notnull(group_df), None).iterrows()
        )


def import_disciplina():
    """Carrega dados de disciplina"""

    print_import_info("Dsiciplina")

    disciplina_df = pd.read_csv("data/disciplina.csv")

    grouped = disciplina_df.groupby(["id_parlamentar_parlametria"])

    for group_index in grouped.groups:
        id_entidade_parlametria = {"id_entidade_parlametria": group_index}

        entidade_relacionada = get_entidade(
            id_entidade_parlametria, "DisciplinaEntidade"
        )

        if entidade_relacionada is None:
            continue

        group_df = (
            grouped.get_group(group_index)[
                [
                    "id_parlamentar",
                    "id_parlamentar_parlametria",
                    "casa",
                    "disciplina"
                ]
            ]
            .assign(entidade=entidade_relacionada)
        )

        Disciplina.objects.bulk_create(
            Disciplina(**r[1].to_dict())
            for r in group_df.where(pd.notnull(group_df), None).iterrows()
        )


def import_votacoes():
    """Carrega votações"""

    print_import_info("Votações")

    votacoes_df = pd.read_csv("data/votacoes.csv")

    votacoes_df["data"] = (
        votacoes_df["data"]
        .astype("str")
        .apply(
            lambda x: None
            if x == "NA"
            else pd.to_datetime(x)
        )
    )

    grouped = votacoes_df.groupby(["id_votacao"])

    for group_index in grouped.groups:

        id_leggo = {"id_leggo": grouped.get_group(group_index)[['id_leggo']].values[0][0]}

        prop = get_proposicao(id_leggo, "Votações")

        group_df = (
            grouped.get_group(group_index)[
                [
                    "id_leggo",
                    "id_votacao",
                    "data",
                    "obj_votacao",
                    "casa",
                    "resumo",
                    "is_nominal"
                ]
            ]
            .assign(proposicao=prop)
        )

        Votacao.objects.bulk_create(
            Votacao(**r[1].to_dict())
            for r in group_df.iterrows()
        )


def get_votacao(votacao_obj, entity_str):
    votacao = None

    try:
        votacao = (
            Votacao.objects.filter(**votacao_obj)
            .first()
        )
    except Exception as e:
        print("Não foi possivel encontrar a votação: {}".format(str(votacao_obj)))
        print("\tErro ao inserir: {}".format(str(entity_str)))
        print("\t{}".format(str(e)))

    return votacao


def import_votos():
    """Carrega votos"""

    print_import_info("Votos")

    votos_df = pd.read_csv("data/votos.csv")

    grouped = votos_df.groupby(["id_votacao", "id_parlamentar_parlametria"])

    for group_index in grouped.groups:
        id_votacao = {"id_votacao": group_index[0]}
        id_entidade_parlametria = {"id_entidade_parlametria": group_index[1]}

        vot = get_votacao(id_votacao, "Voto")
        parlamentar = get_entidade(id_entidade_parlametria, "Voto")

        group_df = (
            grouped.get_group(group_index)
            .assign(votacao=vot)
            .assign(entidade=parlamentar)
        )

        Voto.objects.bulk_create(
            Voto(**r[1].to_dict())
            for r in group_df.iterrows()
        )


def import_anotacoes():
    import_anotacoes_especificas()
    import_anotacoes_gerais()


def import_all_data():
    """Importa dados dos csv e salva no banco."""
    import_entidades()
    import_etapas_proposicoes()
    import_proposicoes()
    import_interesse()
    import_tramitacoes()
    import_temperaturas()
    import_progresso()
    import_pautas()
    import_emendas()
    import_comissoes()
    import_atores()
    import_pressao()
    import_coautoria_node()
    import_coautoria_edge()
    import_autoria()
    import_autores_proposicoes()
    import_relatores_proposicoes()
    import_anotacoes()
    import_destaques()
    # import_votacoes()
    # import_votos()
    import_governismo()
    import_disciplina()


def import_all_data_but_insights():
    """Importa dados dos csv e salva no banco (menos os insights)."""
    import_entidades()
    import_etapas_proposicoes()
    import_proposicoes()
    import_interesse()
    import_tramitacoes()
    import_temperaturas()
    import_progresso()
    import_pautas()
    import_emendas()
    import_comissoes()
    import_atores()
    import_pressao()
    import_coautoria_node()
    import_coautoria_edge()
    import_autoria()
    import_autores_proposicoes()
    import_relatores_proposicoes()
    import_destaques()
    # import_votacoes()
    # import_votos()
    import_governismo()
    import_disciplina()


def import_insights():
    import_anotacoes()
