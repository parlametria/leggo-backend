from django.db import models
from api.model.proposicao import Proposicao
from api.model.etapa_proposicao import Choices
from api.model.interesse import Interesse


class Pressao(models.Model):
    '''
    Pressao da proposicao
    '''

    id_leggo = models.IntegerField('Id da proposição principal no leggo.')
    id_ext = models.IntegerField(
        'ID Externo', default=-1, help_text='Id externo do sistema da casa.')

    casas = Choices('camara senado')
    casa = models.CharField(
        max_length=6, choices=casas.items(), default='',
        help_text='Casa.')

    interesse = models.TextField(blank=True, null=True,
                                 help_text='Interesse da proposição')

    date = models.DateField('Dia da popularidade')

    trends_max_pressao_principal = models.FloatField(
        'Pressão do nome formal e do apelido', default=0)

    trends_max_pressao_rel = models.FloatField(
        'Pressão dos termos relacionados', default=0)

    trends_max_popularity = models.FloatField(
        'Pressão máxima entre os termos', default=0)

    twitter_mean_popularity = models.FloatField(
        'Pressão no twitter', default=0)

    popularity = models.FloatField(
        'Pressão combinada do Twitter e Google Trends',
        default=0)

    proposicao = models.ForeignKey(
        Proposicao, on_delete=models.CASCADE, related_name='pressao')

    interesse_relacionado = models.ForeignKey(
        Interesse, on_delete=models.CASCADE, related_name='pressaoInteresse', null=True)
