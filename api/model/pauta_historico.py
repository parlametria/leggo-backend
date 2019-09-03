
from django.db import models
from api.model.etapa_proposicao import EtapaProposicao


class PautaHistorico(models.Model):
    '''
    Histórico das pautas de uma proposição
    '''

    data = models.DateTimeField('data')

    semana = models.IntegerField('semana')

    local = models.TextField(blank=True)

    em_pauta = models.NullBooleanField(
        help_text='TRUE se a proposicao estiver em pauta, FALSE caso contrario')

    proposicao = models.ForeignKey(
        EtapaProposicao, on_delete=models.CASCADE, related_name='pauta_historico')

    class Meta:
        ordering = ('-data',)
        get_latest_by = '-data'
