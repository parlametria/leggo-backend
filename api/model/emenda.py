from django.db import models
from math import isnan
from api.model.etapa_proposicao import EtapaProposicao


class Emendas(models.Model):
    '''
    Emendas de uma proposição
    '''

    data_apresentacao = models.DateField('data',
        help_text='Data de apresentação da emenda')

    codigo_emenda = models.TextField(blank=True,
        help_text='Código da emenda na casa correspondente')

    distancia = models.FloatField(null=True,
        help_text='Distância calculada entre a emenda e o texto original')

    local = models.TextField(blank=True,
        help_text='Local de apresentação da emenda')

    autor = models.TextField(blank=True,
        help_text='Autor da emenda')

    tipo_documento = models.TextField(
        help_text='Tipo de documento')

    numero = models.FloatField(
        help_text='Número da emenda')

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
