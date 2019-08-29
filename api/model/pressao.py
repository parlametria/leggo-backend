from django.db import models
from api.model.etapa_proposicao import EtapaProposicao
class Pressao(models.Model):
    '''
    Pressao da proposicao
    '''

    date = models.DateField('Dia da popularidade')

    max_pressao_principal = models.FloatField(
        'Pressão do nome formal e do apelido')

    max_pressao_rel = models.FloatField(
        'Pressão dos termos relacionados')

    maximo_geral = models.FloatField(
        'Pressão dos termos relacionados')

    proposicao = models.ForeignKey(
        EtapaProposicao, on_delete=models.CASCADE, related_name='pressao')