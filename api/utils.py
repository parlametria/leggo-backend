import pandas as pd
import numpy as np
from api.models import Proposicao, TramitacaoEvent, EnergiaHistorico, Progresso


def import_all_data():
    ''' 
    Importa dados dos csv e salva no banco.
    '''
    # Carrega proposições
    props_df = (
        pd.read_csv('data/proposicoes.csv', decimal=',')
        .assign(data_apresentacao=lambda x: x.data_apresentacao.apply(
            lambda s: s.split('T')[0]))
    )
    props_df.casa = props_df.casa.apply(lambda r: Proposicao.casas[r])
    Proposicao.objects.bulk_create(
        Proposicao(**r[1].to_dict()) for r in props_df.iterrows())

    # Carrega tramitações
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
            .assign(proposicao=Proposicao.objects.get(**prop_id))
        )
        TramitacaoEvent.objects.bulk_create(
            TramitacaoEvent(**r[1].to_dict()) for r in group_df.iterrows())

    # Carrega históricos de energia
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
            .assign(proposicao=Proposicao.objects.get(**prop_id))
        )
        EnergiaHistorico.objects.bulk_create(
        EnergiaHistorico(**r[1].to_dict()) for r in group_df.iterrows())

    
    # Carrega progresso
    progresso_df = pd.read_csv('data/progressos.csv')

    print(progresso_df.dtypes)

    
    progresso_df['data_inicio'] = progresso_df['data_inicio'].astype('str').apply(lambda x: np.nat if x == "NA" else pd.to_datetime(x.split('T')[0], format='%Y-%m-%d'))
    progresso_df['data_fim'] = progresso_df['data_fim'].astype('str').apply(lambda x: np.nat if x == "NA" else pd.to_datetime(x.split('T')[0], format='%Y-%m-%d'))

    print(progresso_df.head())

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
            .assign(proposicao=Proposicao.objects.get(**prop_id))
        )
        Progresso.objects.bulk_create(
            Progresso(**r[1].to_dict()) for r in group_df.iterrows())

