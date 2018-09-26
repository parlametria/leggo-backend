from munch import Munch
from django.db import models
from django.forms.models import model_to_dict
import datetime

urls = {
    'camara': 'http://www.camara.gov.br/proposicoesWeb/fichadetramitacao?idProposicao=',
    'senado': 'https://www25.senado.leg.br/web/atividade/materias/-/materia/'
}


class Choices(Munch):
    def __init__(self, choices):
        super().__init__({i: i for i in choices.split(' ')})


class Proposicao(models.Model):
    id_ext = models.IntegerField(
        'ID Externo',
        help_text='Id externo do sistema da casa.')

    numero = models.IntegerField(
        'Número',
        help_text='Número da proposição naquele ano e casa.')

    sigla_tipo = models.CharField(
        'Sigla do Tipo', max_length=3,
        help_text='Sigla do tipo da proposição (PL, PLS etc)')

    data_apresentacao = models.DateField('Data de apresentação')

    casas = Choices('camara senado')
    casa = models.CharField(
        max_length=6, choices=casas.items(),
        help_text='Casa desta proposição.')

    regimes = Choices('ordinario prioridade urgencia')
    regime_tramitacao = models.CharField(
        'Regime de tramitação',
        max_length=10, choices=regimes.items(), null=True)

    formas_apreciacao = Choices('conclusiva plenario')
    forma_apreciacao = models.CharField(
        'Forma de Apreciação',
        max_length=10, choices=formas_apreciacao.items(), null=True)

    ementa = models.TextField(blank=True)

    justificativa = models.TextField(blank=True)

    palavras_chave = models.TextField(blank=True)

    casa_origem = models.TextField(blank=True)

    autor_nome = models.TextField(blank=True)

    energia = models.FloatField(null=True)

    em_pauta = models.NullBooleanField(
        help_text='TRUE se a proposicao estará em pauta na semana, FALSE caso contrario')

    apelido = models.CharField(
        'Apelido da proposição.', max_length=60,
        help_text='Apelido dado para proposição.', null=True)

    tema = models.TextField(
        'Tema da proposição.', max_length=40,
        help_text='Podendo ser entre Meio Ambiente e agenda nacional.', null=True)

    class Meta:
        indexes = [
            models.Index(fields=['casa', 'id_ext']),
        ]
        ordering = ('-data_apresentacao',)

    @property
    def sigla(self):
        '''Sigla da proposição (ex.: PL 400/2010)'''
        return f'{self.sigla_tipo} {self.numero}/{self.ano}'

    @property
    def ano(self):
        return self.data_apresentacao.year

    @property
    def url(self):
        '''URL para a página da proposição em sua respectiva casa.'''
        return urls[self.casa] + str(self.id_ext)

    @property
    def resumo_tramitacao(self):
        locais = []
        events = []
        for event in self.tramitacao.all():
            if event.sigla_local not in locais:
                locais.append(event.sigla_local)
                events.append({
                    'data': event.data,
                    'casa': event.proposicao.casa,
                    'nome': event.sigla_local
                })
        return events
    
    # Retorna energia recente dos últimos 'num_dias'
    def energia_recente(self, num_dias=90):
        energias = []
        now = datetime.datetime.now()
        for energia in self.energia_recente_periodo.all():
            if((not num_dias) or (now.date() - energia.periodo).days <= num_dias):
                energias.append({
                    'periodo': energia.periodo,
                    'energia_periodo': energia.energia_periodo,
                    'energia_recente': energia.energia_recente
                })
                       
        return energias

class TramitacaoEvent(models.Model):

    data = models.DateField('Data')

    sequencia = models.IntegerField(
        'Sequência',
        help_text='Sequência desse evento na lista de tramitações.')

    texto = models.TextField()

    sigla_local = models.TextField()

    situacao = models.TextField()

    proposicao = models.ForeignKey(
        Proposicao, on_delete=models.CASCADE, related_name='tramitacao')

    class Meta:
        ordering = ('sequencia',)

class EnergiaRecentePeriodo(models.Model):
    periodo = models.DateField('periodo')

    energia_periodo = models.IntegerField(help_text='Quantidade de eventos no período (semana)')

    energia_recente = models.FloatField(help_text='Energia acumulada com decaimento exponencial')

    proposicao = models.ForeignKey(
        Proposicao, on_delete=models.CASCADE, related_name='energia_recente_periodo')

    class Meta:
        ordering = ('periodo',)
