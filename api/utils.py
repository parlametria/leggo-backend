import pandas as pd
from api.models import (
    EtapaProposicao, TramitacaoEvent, EnergiaHistorico, Progresso, Proposicao)


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
    grouped = pd.read_csv('data/trams.csv').groupby(['casa', 'id_ext'])
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
            [['data', 'sequencia', 'sigla_local', 'situacao']]
            .assign(proposicao=EtapaProposicao.objects.get(**prop_id))
        )
        TramitacaoEvent.objects.bulk_create(
            TramitacaoEvent(**r[1].to_dict()) for r in group_df.iterrows())


def import_energias():
    '''Carrega históricos de energia'''
    grouped = pd.read_csv('data/hists_energia.csv').groupby(['casa', 'id_ext'])
    for group_index in grouped.groups:
        prop_id = {
            'casa': group_index[0],
            'id_ext': group_index[1],
        }
        group_df = (
            grouped
            .get_group(group_index)
            .assign(periodo=lambda x: x.periodo.apply(lambda s: s.split('T')[0]))
            [['periodo', 'energia_periodo', 'energia_recente']]
            .assign(proposicao=EtapaProposicao.objects.get(**prop_id))
        )
        EnergiaHistorico.objects.bulk_create(
            EnergiaHistorico(**r[1].to_dict()) for r in group_df.iterrows())


def import_progresso():
    '''Carrega progresso'''
    progresso_df = pd.read_csv('data/progressos.csv')

    progresso_df['data_inicio'] = progresso_df['data_inicio'].astype('str').apply(
        lambda x:
        None if x == "NA" else pd.to_datetime(x.split('T')[0], format='%Y-%m-%d')
    )
    progresso_df['data_fim'] = progresso_df['data_fim'].astype('str').apply(
        lambda x:
        None if x == "NA" else pd.to_datetime(x.split('T')[0], format='%Y-%m-%d')
    )

    grouped = progresso_df.groupby(['casa', 'id_ext'])

    for group_index in grouped.groups:
        prop_id = {
            'casa': group_index[0],
            'id_ext': group_index[1],
        }
        group_df = (
            grouped
            .get_group(group_index)
            .filter(['data_inicio', 'data_fim', 'local', 'fase_global', 'local_casa'])
            .assign(etapa=EtapaProposicao.objects.get(**prop_id))
            .assign(data_inicio=lambda x: x.data_inicio.astype('object'))
            .assign(data_fim=lambda x: x.data_fim.astype('object'))
        )
        Progresso.objects.bulk_create(
            Progresso(**r[1].to_dict())
            for r in group_df.where(pd.notnull(group_df), None).iterrows())


def import_all_data():
    '''Importa dados dos csv e salva no banco.'''
    import_etapas_proposicoes()
    import_proposicoes()
    import_tramitacoes()
    import_energias()
    import_progresso()
