from django.db import models
from api.model.proposicao import Proposicao


class Interesse(models.Model):
    '''
    Interesses analisados e relacionados as PL's
    '''

    id_leggo = models.IntegerField(
        help_text='Id da proposição no Leggo.')

    interesse = models.TextField(
        help_text='Interesse da PL')

    proposicao = models.ForeignKey(
        Proposicao, on_delete=models.CASCADE, related_name='interesse')
