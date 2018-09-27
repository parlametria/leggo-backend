import pandas as pd
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
    grouped = pd.read_csv('data/progressos.csv').dropna()
    grouped = grouped.groupby(['casa', 'id_ext'])
    for group_index in grouped.groups: 
        prop_id = {
            'casa': group_index[0],
            'id_ext': group_index[1],
        }
        group_df = (
            grouped
            .get_group(group_index)
            .assign(
            data_inicio=lambda x: x.data_inicio.apply(
            lambda s: s.split('T')[0]))
            .assign(
                data_fim=lambda x: x.data_fim.apply(
                lambda s: s.split('T')[0]))
            [['data_inicio', 'data_fim', 'local', 'fase_global', 'local_casa']]
            .assign(proposicao=Proposicao.objects.get(**prop_id))
        )
        Progresso.objects.bulk_create(
            Progresso(**r[1].to_dict()) for r in group_df.iterrows())