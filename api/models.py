from munch import Munch
from django.db import models

URLS = {
    'camara': 'http://www.camara.gov.br/proposicoesWeb/fichadetramitacao?idProposicao=',
    'senado': 'https://www25.senado.leg.br/web/atividade/materias/-/materia/'
}

ORDER_PROGRESSO = [
    ('Construção', 'Comissões'),
    ('Construção', 'Plenário'),
    ('Revisão I', 'Comissões'),
    ('Revisão I', 'Plenário'),
    ('Revisão II', 'Comissões'),
    ('Revisão II', 'Plenário'),
    ('Sansão/Veto', 'Presidência da República'),
    ('Avaliação dos Vetos', 'Congresso'),
]


class Choices(Munch):
    def __init__(self, choices):
        super().__init__({i: i for i in choices.split(' ')})


class Proposicao(models.Model):

    apelido = models.TextField(blank=True)
    tema = models.TextField(blank=True)

    @property
    def resumo_progresso(self):
        return sorted(
            [{
                'fase_global': progresso.fase_global,
                'local': progresso.local,
                'data_inicio': progresso.data_inicio,
                'data_fim': progresso.data_fim,
                'local_casa': progresso.local_casa,
                'pulou': progresso.pulou
            } for progresso in self.progresso.all()],
            key=lambda x: ORDER_PROGRESSO.index((x['fase_global'], x['local'])))


class EtapaProposicao(models.Model):
    id_ext = models.IntegerField(
        'ID Externo',
        help_text='Id externo do sistema da casa.')

    proposicao = models.ForeignKey(
        Proposicao, on_delete=models.CASCADE, related_name='etapas', null=True)

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

    autor_nome = models.TextField(blank=True)

    relator_nome = models.TextField(blank=True)

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
        ordering = ('data_apresentacao',)

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
        return URLS[self.casa] + str(self.id_ext)

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


class TramitacaoEvent(models.Model):

    data = models.DateField('Data')

    sequencia = models.IntegerField(
        'Sequência',
        help_text='Sequência desse evento na lista de tramitações.')

    texto = models.TextField()

    sigla_local = models.TextField()

    situacao = models.TextField()

    proposicao = models.ForeignKey(
        EtapaProposicao, on_delete=models.CASCADE, related_name='tramitacao')

    class Meta:
        ordering = ('sequencia',)


class EnergiaHistorico(models.Model):
    '''
    Histórico de energia de uma proposição
    '''
    periodo = models.DateField('periodo')

    energia_periodo = models.IntegerField(
        help_text='Quantidade de eventos no período (semana).')

    energia_recente = models.FloatField(
        help_text='Energia acumulada com decaimento exponencial.')

    proposicao = models.ForeignKey(
        EtapaProposicao, on_delete=models.CASCADE, related_name='energia_historico')

    class Meta:
        ordering = ('-periodo',)
        get_latest_by = '-periodo'

class PautaHistorico(models.Model):
    '''
    Histórico das pautas de uma proposição
    '''

    data = models.DateField('data')

    sigla = models.TextField(blank=True)

    id_ext = models.IntegerField(
        'ID Externo',
        help_text='Id externo do sistema da casa.',
        blank=False)
    
    local = models.TextField(blank=True)

    casa = models.TextField(blank=True)

    em_pauta = models.NullBooleanField(
        help_text='TRUE se a proposicao estiver em pauta naquela semana, FALSE caso contrario')

    semana = models.IntegerField(
        help_text='Qual a semana do ano que está')

    ano = models.IntegerField(
        help_text='Qual o ano da agenda')

    proposicao = models.ForeignKey(
        EtapaProposicao, on_delete=models.CASCADE, related_name='pauta_historico')

    class Meta:
        ordering = ('-data',)
        get_latest_by = '-data'


class Progresso(models.Model):

    local_casa = models.CharField(
        max_length=30,
        help_text='Casa desta proposição.',
        null=True)

    fase_global = models.TextField(blank=True)

    local = models.TextField(blank=True, null=True)

    data_inicio = models.DateField('Data de início', null=True, blank=True)

    data_fim = models.DateField('Data final', null=True, blank=True)

    proposicao = models.ForeignKey(
       Proposicao, on_delete=models.CASCADE, related_name='progresso')

    pulou = models.NullBooleanField(
        help_text='TRUE se a proposicao pulou a fase, FALSE caso contrario')
