import os
import time
from datetime import datetime
import pandas as pd
from scipy import stats
from api.models import (
    EtapaProposicao, TramitacaoEvent, TemperaturaHistorico,
    Progresso, Proposicao, PautaHistorico, Emendas, InfoGerais)


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
    props_df = pd.read_csv('data/tabela_geral_ids_casa.csv')

    for r in props_df.iterrows():
        data = r[1].to_dict()
        etapas = []
        for casa in ['camara', 'senado']:
            id_ext = data.pop(f'id_{casa}')
            if pd.notna(id_ext):
                etapa_id = {
                    'casa': casa,
                    'id_ext': id_ext
                }
                etapas.append(EtapaProposicao.objects.get(**etapa_id))
        prop = Proposicao(**data)
        prop.save()
        prop.etapas.set(etapas)
        prop.save()


def import_tramitacoes():
    '''Carrega tramitações'''
    filepath = 'data/trams.csv'
    grouped = pd.read_csv(filepath).groupby(['casa', 'id_ext'])
    for group_index in grouped.groups:
        prop_id = {
            'casa': group_index[0],
            'id_ext': group_index[1],
        }
        group_df = (
            grouped
            .get_group(group_index)
            .assign(descricao=lambda x: x.descricao_situacao)
            .assign(data=lambda x: x.data.apply(lambda s: s.split('T')[0]))
            .assign(situacao=lambda x: x.descricao_situacao)
            [['data', 'sequencia', 'evento', 'sigla_local', 'local', 'situacao',
                'texto_tramitacao', 'status']]
            .assign(proposicao=EtapaProposicao.objects.get(**prop_id))
        )
        TramitacaoEvent.objects.bulk_create(
            TramitacaoEvent(**r[1].to_dict()) for r in group_df.iterrows())

    last_update = datetime.utcfromtimestamp(os.path.getmtime(filepath))
    InfoGerais.objects.create(name='last_update_trams', value=last_update.isoformat())


def import_temperaturas():
    '''Carrega históricos de temperatura'''
    grouped = pd.read_csv('data/hists_temperatura.csv').groupby(['casa', 'id_ext'])
    for group_index in grouped.groups:
        prop_id = {
            'casa': group_index[0],
            'id_ext': group_index[1],
        }
        group_df = (
            grouped
            .get_group(group_index)
            .assign(periodo=lambda x: x.periodo.apply(lambda s: s.split('T')[0]))
            .filter(['periodo', 'temperatura_periodo', 'temperatura_recente'])
            .assign(proposicao=EtapaProposicao.objects.get(**prop_id))
        )
        TemperaturaHistorico.objects.bulk_create(
            TemperaturaHistorico(**r[1].to_dict()) for r in group_df.iterrows())


def import_pautas():
    '''Carrega históricos de pautas'''
    grouped = pd.read_csv('data/pautas.csv').groupby(['casa', 'id_ext'])
    for group_index in grouped.groups:
        prop_id = {
            'casa': group_index[0],
            'id_ext': group_index[1],
        }
        group_df = (
            grouped
            .get_group(group_index)
            .assign(proposicao=EtapaProposicao.objects.get(**prop_id))
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
        group_df = (
            grouped
            .get_group(group_index)
            .filter(['data_inicio', 'data_fim',
                     'local', 'fase_global', 'local_casa', 'pulou'])
            .assign(proposicao=EtapaProposicao.objects.get(**prop_id).proposicao)
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
        group_df = (
            emendas_df
            .get_group(group_index)
            [['data_apresentacao', 'local', 'autor']]
            .assign(proposicao=EtapaProposicao.objects.get(**prop_id))
        )
        Emendas.objects.bulk_create(
            Emendas(**r[1].to_dict()) for r in group_df.iterrows())


def import_all_data():
    '''Importa dados dos csv e salva no banco.'''
    import_etapas_proposicoes()
    import_proposicoes()
    import_tramitacoes()
    import_temperaturas()
    import_progresso()
    import_pautas()
    import_emendas()


def get_coefficient_temperature(temperatures):
    '''
    Calcula coeficiente linear das temperaturas nas últims 6 semanas
    '''
    dates_x = [datetime_to_timestamp(temperatura.periodo)
               for temperatura in temperatures[:6]]
    temperaturas_y = [temperatura.temperatura_recente for temperatura in temperatures[:6]]

    if(dates_x and temperaturas_y and len(dates_x) > 1 and len(temperaturas_y) > 1):
        return stats.linregress(dates_x, temperaturas_y)[0]
    else:
        return 0


def datetime_to_timestamp(date):
    return time.mktime(date.timetuple())
