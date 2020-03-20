from django.db import models
from api.model.proposicao import Proposicao


class Interesse(models.Model):
    '''
    Interesses analisados e relacionados as PL's
    '''    

    id_ext = models.IntegerField(
        help_text='Id externo da proposição na casa correspondente.')

    casa = models.TextField(
        help_text='Casa de tramitação da proposição.')

    id_leggo = models.TextField(
        help_text='Id da proposição no Leggo.')

    interesse = models.TextField(
        help_text='Interesse da PL')

    proposicao = models.ForeignKey(
        Proposicao, on_delete=models.CASCADE, related_name='interesse')
