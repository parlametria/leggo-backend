import os
import datetime
import pandas as pd
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


def import_etapas_proposicoes():
    '''Carrega etapas das proposições'''
    props_df = (
        pd.read_csv('data/proposicoes.csv', decimal=',')
        .assign(data_apresentacao=lambda x: x.data_apresentacao.apply(
            lambda s: s.split('T')[0]))
    )
    props_df.casa = props_df.casa.apply(lambda r: EtapaProposicao.casas[r])
    EtapaProposicao.objects.bulk_create(
        EtapaProposicao(**r[1].to_dict()) for r in props_df.iterrows())


def import_proposicoes():
    '''Carrega proposições'''
    props_df = pd.read_csv('data/proposicoes.csv')

    for _, etapas_df in props_df.groupby('apelido'):
        etapas = []
        for _, etapa in etapas_df.iterrows():
            etapas.append(
                EtapaProposicao.objects.get(casa=etapa.casa, id_ext=etapa.id_ext))
        prop = Proposicao(apelido=etapa.apelido, tema=etapa.tema, id_leggo=etapa.id_leggo)
        prop.save()
        prop.etapas.set(etapas)
        prop.save()


def import_tramitacoes():
    '''Carrega tramitações'''
    filepath = 'data/trams.csv'
    grouped = pd.read_csv(filepath).groupby(['casa', 'id_ext'])

    col_names = [
        'data', 'sequencia', 'evento', 'titulo_evento', 'sigla_local', 'local', 'nivel',
        'situacao', 'texto_tramitacao', 'status', 'tipo_documento', 'link_inteiro_teor']

    for group_index in grouped.groups:
        prop_id = {
            'casa': group_index[0],
            'id_ext': group_index[1],
        }

        etapa_prop = get_etapa_proposicao(prop_id)

        if etapa_prop is None:
            continue

        group_df = (
            grouped
            .get_group(group_index)
            # renomeios
            .assign(descricao=lambda x: x.descricao_situacao)
            .assign(situacao=lambda x: x.descricao_situacao)
            # pega apenas a data e não a hora
            .assign(data=lambda x: x.data.apply(lambda s: s.split('T')[0]))
            # eventos sem nível recebem o maior valor (ou seja, são menos importantes)
            .assign(nivel=lambda x: x.nivel.fillna(x.nivel.max()))
            # filtra deixando apenas as colunas desejadas
            .pipe(lambda x: x.loc[:, x.columns.isin(col_names)])
            # adiciona referência para a correspondente etapa da proposição
            .assign(etapa_proposicao=etapa_prop)
        )
        TramitacaoEvent.objects.bulk_create(
            TramitacaoEvent(**r[1].to_dict()) for r in group_df.iterrows())

    last_update = datetime.datetime.utcfromtimestamp(os.path.getmtime(filepath))
    InfoGerais.objects.create(name='last_update_trams', value=last_update.isoformat())


def import_temperaturas():
    '''Carrega históricos de temperatura'''
    grouped = pd.read_csv('data/hists_temperatura.csv').groupby(['id_leggo'])
    for group_index in grouped.groups:
        id_leggo = {
            'id_leggo': group_index
        }

        prop = get_proposicao(id_leggo)

        if prop is None:
            continue

        group_df = (
            grouped
            .get_group(group_index)
            .assign(periodo=lambda x: x.periodo.apply(lambda s: s.split('T')[0]))
            .filter(['periodo', 'temperatura_periodo', 'temperatura_recente'])
            .assign(proposicao=prop)
        )
        TemperaturaHistorico.objects.bulk_create(
            TemperaturaHistorico(**r[1].to_dict()) for r in group_df.iterrows())


def import_coautoria_node():
    '''Carrega nós'''
    grouped = pd.read_csv('data/coautorias_nodes.csv').groupby(['id_leggo'])
    for group_index in grouped.groups:
        id_leggo = {
            'id_leggo': group_index
        }

        prop = get_proposicao(id_leggo)

        if prop is None:
            continue

        group_df = (
            grouped
            .get_group(group_index)
        )
        CoautoriaNode.objects.bulk_create(
            CoautoriaNode(**r[1].to_dict()) for r in group_df.iterrows())


def import_coautoria_edge():
    '''Carrega arestas'''
    grouped = pd.read_csv('data/coautorias_edges.csv').groupby(['id_leggo'])
    for group_index in grouped.groups:
        id_leggo = {
            'id_leggo': group_index
        }

        prop = get_proposicao(id_leggo)

        if prop is None:
            continue

        group_df = (
            grouped
            .get_group(group_index)
        )
        CoautoriaEdge.objects.bulk_create(
            CoautoriaEdge(**r[1].to_dict()) for r in group_df.iterrows())


def import_pautas():
    '''Carrega históricos de pautas'''
    grouped = pd.read_csv('data/pautas.csv').groupby(['casa', 'id_ext'])
    for group_index in grouped.groups:
        prop_id = {
            'casa': group_index[0],
            'id_ext': group_index[1],
        }

        etapa_prop = get_etapa_proposicao(prop_id)

        if etapa_prop is None:
            continue

        group_df = (
            grouped
            .get_group(group_index)
            .assign(proposicao=etapa_prop)
            .filter(['data', 'semana', 'local', 'em_pauta', 'proposicao'])
        )
        PautaHistorico.objects.bulk_create(
            PautaHistorico(**r[1].to_dict()) for r in group_df.iterrows())


def import_progresso():
    '''Carrega o progresso das proposições'''
    progresso_df = pd.read_csv('data/progressos.csv')

    for col in ['data_inicio', 'data_fim']:
        progresso_df[col] = progresso_df[col].astype('str').apply(
            lambda x:
            None if x == 'NA' else pd.to_datetime(x.split('T')[0], format='%Y-%m-%d')
        )

    grouped = progresso_df.groupby(['casa', 'id_ext'])

    for group_index in grouped.groups:
        if any(map(pd.isna, group_index)):
            print('Aviso: dados de progresso possuem NAN nos identificadores!')
            continue
        prop_id = {
            'casa': group_index[0],
            'id_ext': group_index[1],
        }

        etapa_prop = get_etapa_proposicao(prop_id)

        if etapa_prop is None:
            continue

        group_df = (
            grouped
            .get_group(group_index)
            .filter(['data_inicio', 'data_fim',
                     'local', 'fase_global', 'local_casa', 'pulou'])
            .assign(proposicao=etapa_prop.proposicao)
            .assign(data_inicio=lambda x: x.data_inicio.astype('object'))
            .assign(data_fim=lambda x: x.data_fim.astype('object'))
        )
        Progresso.objects.bulk_create(
            Progresso(**r[1].to_dict())
            for r in group_df.where(pd.notnull(group_df), None).iterrows())


def import_emendas():
    '''Carrega emendas'''
    emendas_df = pd.read_csv('data/emendas.csv').groupby(['casa', 'id_ext'])
    for group_index in emendas_df.groups:
        prop_id = {
            'casa': group_index[0],
            'id_ext': group_index[1],
        }

        etapa_prop = get_etapa_proposicao(prop_id)

        if etapa_prop is None:
            continue

        group_df = (
            emendas_df
            .get_group(group_index)
            [['codigo_emenda', 'numero', 'distancia', 'tipo_documento',
              'data_apresentacao', 'local', 'autor', 'inteiro_teor']]
            .assign(proposicao=etapa_prop)
        )
        Emendas.objects.bulk_create(
            Emendas(**r[1].to_dict()) for r in group_df.iterrows())


def import_atores():
    '''Carrega Atores'''
    atores_df = pd.read_csv('data/atores.csv').groupby(['id_leggo', 'casa', 'id_ext'])
    for group_index in atores_df.groups:
        prop_id = {
            'casa': group_index[1],
            'id_ext': group_index[2],
        }

        etapa_prop = get_etapa_proposicao(prop_id)

        if etapa_prop is None:
            continue

        group_df = (
            atores_df
            .get_group(group_index)
            [['id_leggo', 'id_ext', 'casa', 'id_autor', 'nome_autor', 'partido', 'uf',
             'peso_total_documentos', 'tipo_generico', 'sigla_local',
              'is_important', 'bancada']]
            .assign(proposicao=etapa_prop)
        )
        Atores.objects.bulk_create(
            Atores(**r[1].to_dict()) for r in group_df.iterrows())


def import_comissoes():
    '''Carrega Comissoes'''
    comissoes_df = pd.read_csv('data/comissoes.csv').groupby(['casa', 'sigla'])
    for group_index in comissoes_df.groups:
        group_df = (
            comissoes_df
            .get_group(group_index)
        )
        Comissao.objects.bulk_create(
            Comissao(**r[1].to_dict()) for r in group_df.iterrows())


def import_pressao():
    '''Carrega pressao das proposicoes'''
    directory = os.fsencode('data/pops')

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        pressao_df = pd.read_csv('data/pops/' + str(filename))
        prop_id = {
            'casa': pressao_df['casa'][0],
            'id_ext': pressao_df['id_ext'][0],
        }

        etapa_prop = get_etapa_proposicao(prop_id)

        if etapa_prop is None:
            continue

        pressao_clean_df = (
            pressao_df
            [['date', 'max_pressao_principal',
              'max_pressao_rel',	'maximo_geral']]
            .assign(proposicao=etapa_prop)
        )

        Pressao.objects.bulk_create(
            Pressao(**r[1].to_dict()) for r in pressao_clean_df.iterrows())


def get_etapa_proposicao(prop_id):
    etapa_prop = None

    try:
        etapa_prop = EtapaProposicao.objects.get(**prop_id)
    except Exception:
        print("Não foi possivel encontrar a etapa proposição: {}".format(str(prop_id)))

    return etapa_prop


def get_proposicao(leggo_id):
    prop = None

    try:
        prop = Proposicao.objects.get(**leggo_id)
    except Exception:
        print("Não foi possivel encontrar a proposição: {}".format(str(leggo_id)))

    return prop


def import_all_data():
    '''Importa dados dos csv e salva no banco.'''
    import_etapas_proposicoes()
    import_proposicoes()
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
