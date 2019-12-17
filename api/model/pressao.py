from django.db import models
from api.model.proposicao import Proposicao


class Pressao(models.Model):
    '''
    Pressao da proposicao
    '''

    id_leggo = models.IntegerField('Id da proposição principal no leggo.')

    date = models.DateField('Dia da popularidade')

    max_pressao_principal = models.FloatField(
        'Pressão do nome formal e do apelido')

    max_pressao_rel = models.FloatField(
        'Pressão dos termos relacionados')

    maximo_geral = models.FloatField(
        'Pressão dos termos relacionados')

    proposicao = models.ForeignKey(
        Proposicao, on_delete=models.CASCADE, related_name='pressao')
