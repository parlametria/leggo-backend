# import os
# from glob import glob
import pandas as pd
from api.models import Proposicao, TramitacaoEvent


def import_all_data():
    # Carrega proposições
    props_df = pd.read_csv('data/proposicoes.csv')
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


# # prop_data_files = '../../agora-digital/data/*/*proposicao*.csv'
# # tram_data_files = '../../agora-digital/data/*/*tramitacao*.csv'
# # visu_data_files = '../../agora-digital/data/vis/tramitacao/*.csv'
# prop_data_files = 'data/*/*prop*.csv'
# visu_data_files = 'data/vis/tramitacao/*.csv'


# def nan_to_none(df):
#     '''Replace NANs with None to avoid JSON error.'''
#     return df.where((pd.notnull(df)), None)


# def simplify_visu(df):
#     fases = []
#     for fase in df[df.group == 'Global'].label.unique():
#         if 'Câmara' in fase:
#             casa = 'camara'
#         elif 'Senado' in fase:
#             casa = 'senado'
#         fases.append({
#             'casa': casa,
#             'nome': fase.split('-')[0].strip()
#         })
#     return fases


# def simplify_tram(id):
#     df = grouped_trams.get_group(id)
#     return 'a'


# # Tramitações
# trams = nan_to_none(
#     pd.concat([pd.read_csv(f) for f in glob(tram_data_files)], sort=False)
#     # TODO: junta as colunas de IDs do Senado e da Câmara, isso deveria estar
#     # sendo feito pelo R...
#     .assign(proposicao=lambda x: (
#         x.codigo_materia.fillna(0) + x.id_prop.fillna(0)).apply(int))
# )
# grouped_trams = trams.groupby('proposicao')

# Timeline data
# visu = (
#     pd.concat([
#         pd.read_csv(f).assign(prop=lambda x: int(os.path.basename(f).split('-')[0]))
#         for f in glob(visu_data_files)
#     ], sort=False)
#     .set_index('prop')
#     .groupby('prop')
#     .apply(simplify_visu)
# )

# # Proposições
# props = nan_to_none(
#     pd.concat([pd.read_csv(f) for f in glob(prop_data_files)], sort=False)
#     # TODO: junta as colunas de IDs do Senado e da Câmara, isso deveria estar
#     # sendo feito pelo R...
#     .assign(id=lambda x: (x.codigo_materia.fillna(0) + x.id.fillna(0)).apply(int))
#     .assign(sigla_tipo=lambda x:
#             x.sigla_subtipo_materia.fillna('') + x.sigla_tipo.fillna(''))
#     .assign(numero=lambda x: x.numero.fillna(0) + x.numero_materia.fillna(0))
#     .assign(data_apresentacao=lambda x: x.data_apresentacao.apply(
#         lambda s: s.split('T')[0]))
#     .assign(casa=lambda x:
#             x.nome_casa_identificacao_materia.fillna('camara').apply(
#                 lambda s: s.split()[0].lower()))
#     .set_index('id', drop=False)
#     .assign(fases=visu)
#     # .assign(tramitacao=lambda x: x.id.apply(simplify_tram))
# )
