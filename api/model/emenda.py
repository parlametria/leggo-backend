from django.db import models
from math import isnan
from api.model.etapa_proposicao import EtapaProposicao


class Emendas(models.Model):
    '''
    Emendas de uma proposição
    '''

    data_apresentacao = models.DateField('data')

    codigo_emenda = models.TextField(blank=True)

    distancia = models.FloatField(null=True)

    local = models.TextField(blank=True)

    autor = models.TextField(blank=True)

    tipo_documento = models.TextField()

    numero = models.FloatField()

    @property
    def titulo(self):
        '''Título da emenda.'''
        numero = self.numero
        if (isnan(numero)):
            numero = ''
        else:
            numero = str(int(numero))
        return (self.tipo_documento + ' ' + numero)

    proposicao = models.ForeignKey(
        EtapaProposicao, on_delete=models.CASCADE, related_name='emendas')

    inteiro_teor = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('-data_apresentacao',)
        get_latest_by = '-data_apresentacao'
