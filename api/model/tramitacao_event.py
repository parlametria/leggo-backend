from django.db import models
from api.model.etapa_proposicao import EtapaProposicao


class TramitacaoEvent(models.Model):
    data = models.DateField('Data')

    sequencia = models.IntegerField(
        'Sequência',
        help_text='Sequência desse evento na lista de tramitações.')

    evento = models.TextField()

    titulo_evento = models.TextField()

    sigla_local = models.TextField(blank=True)

    local = models.TextField()

    situacao = models.TextField()

    texto_tramitacao = models.TextField()

    status = models.TextField()

    tipo_documento = models.TextField()

    link_inteiro_teor = models.TextField(blank=True, null=True)

    etapa_proposicao = models.ForeignKey(
        EtapaProposicao, on_delete=models.CASCADE, related_name='tramitacao')

    nivel = models.IntegerField(
        blank=True, null=True,
        help_text='Nível de importância deste evento para notificações.')

    temperatura_local = models.FloatField(
        blank=True, null=True,
        help_text='Temperatura do local do evento.')

    temperatura_evento = models.FloatField(
        blank=True, null=True,
        help_text='Temperatura do evento.')

    @property
    def casa(self):
        '''Casa onde o evento ocorreu.'''
        return self.proposicao.casa

    @property
    def proposicao_id(self):
        '''ID da proposição no sistema leggo a qual esse evento se refere.'''
        return self.etapa_proposicao.proposicao.id_leggo

    @property
    def proposicao(self):
        '''Proposição a qual esse evento se refere.'''
        return self.etapa_proposicao.proposicao

    @property
    def tema(self):
        '''Tema a qual esse evento se refere.'''
        return self.etapa_proposicao.tema

    class Meta:
        ordering = ('data', 'sequencia')
