import time
from scipy import stats
from munch import Munch
from django.db import models
from django.contrib.postgres.fields import JSONField
# from api.utils.temperatura import get_coefficient_temperature

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
    ('Sanção/Veto', 'Presidência da República'),
    ('Avaliação dos Vetos', 'Congresso'),
]


class Choices(Munch):
    def __init__(self, choices):
        super().__init__({i: i for i in choices.split(' ')})


class InfoGerais(models.Model):

    name = models.TextField()
    value = JSONField()


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
            } for progresso in self.progresso.exclude(fase_global__icontains='Pré')],
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

    autor_uf = models.TextField(blank=True)
    
    autor_partido = models.TextField(blank=True)
    
    relator_nome = models.TextField(blank=True)

    casa_origem = models.TextField(blank=True)

    temperatura = models.FloatField(null=True)

    em_pauta = models.NullBooleanField(
        help_text='TRUE se a proposicao estará em pauta na semana, FALSE caso contrario')

    apelido = models.TextField(
        'Apelido da proposição.',
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
    def autores(self):
        nomes = self.autor_nome.split("+")
        partidos = self.autor_partido.split("+")
        ufs = self.autor_uf.split("+")

        autores = []
        for i in range(len(nomes)):
            autor = nomes[i].strip()
            if "Poder Executivo" in autor or "Presidência" in autor:
                autores.append(autor)
            elif "Senado Federal" in autor:
                senado = autor.split(" - ")
                if "Comissão" in senado[-1]:
                    autores.append("Sen. " + senado[-1])
                else:
                    autores.append('Sen. ' + senado[-1] + " (" + partidos[i] + "-" + ufs[i] + ")")
            elif "Legislação" in autor:
                autores.append("Câm. " + autor)
            else:
                autores.append("Dep. " + autor + " (" + partidos[i] + "-" + ufs[i] + ")")

        return autores 
    
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
    def temperatura_coeficiente(self):
        '''
        Calcula coeficiente linear das temperaturas nas últimas 6 semanas.
        '''
        temperatures = self.temperatura_historico.all()[:6]
        dates_x = [
            time.mktime(temperatura.periodo.timetuple())
            for temperatura in temperatures]
        temperaturas_y = [
            temperatura.temperatura_recente
            for temperatura in temperatures]

        if (dates_x and temperaturas_y and len(dates_x) > 1 and len(temperaturas_y) > 1):
            return stats.linregress(dates_x, temperaturas_y)[0]
        else:
            return 0

    @property
    def status(self):
        if (hasattr(self, '_prefetched_objects_cache')
           and 'tramitacao' in self._prefetched_objects_cache):
            # It's pefetched, avoid query
            trams = list(self.tramitacao.all())
            if trams:
                return trams[-1].status
            else:
                return None
        else:
            # Not prefetched, query
            return self.tramitacao.last().status

    @property
    def resumo_tramitacao(self):
        locais = []
        events = []
        local = ""
        for event in self.tramitacao.all():
            if event.local == "Comissões":
                locais.append(event.sigla_local)
                events.append({
                    'data': event.data,
                    'casa': event.etapa_proposicao.casa,
                    'local': event.sigla_local,
                    'evento': event.evento,
                    'texto_tramitacao': event.texto_tramitacao,
                    'link_inteiro_teor': event.link_inteiro_teor
                })
            else:
                if event.local != local:
                    local = event.local
                    events.append({
                        'data': event.data,
                        'casa': event.etapa_proposicao.casa,
                        'local': event.sigla_local,
                        'evento': event.evento,
                        'texto_tramitacao': event.texto_tramitacao,
                        'link_inteiro_teor': event.link_inteiro_teor
                    })
        return sorted(events, key=lambda k: k['data'])

    @property
    def comissoes_passadas(self):
        '''
        Pega todas as comissões nas quais a proposição já
        tramitou
        '''
        comissoes = set()
        local_com_c_que_nao_e_comissao = "CD-MESA-PLEN"
        for row in self.tramitacao.all():
            if row.local != local_com_c_que_nao_e_comissao and row.local[0] == "C":
                comissoes.add(row.local)
        return comissoes


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

    @property
    def casa(self):
        '''Casa onde o evento ocorreu.'''
        return self.proposicao.casa

    @property
    def proposicao_id(self):
        '''ID da proposição a qual esse evento se refere.'''
        return self.etapa_proposicao.proposicao_id

    @property
    def proposicao(self):
        '''Proposição a qual esse evento se refere.'''
        return self.etapa_proposicao.proposicao

    class Meta:
        ordering = ('data', 'sequencia')


class TemperaturaHistorico(models.Model):
    '''
    Histórico de temperatura de uma proposição
    '''
    periodo = models.DateField('periodo')

    temperatura_periodo = models.IntegerField(
        help_text='Quantidade de eventos no período (semana).')

    temperatura_recente = models.FloatField(
        help_text='Temperatura acumulada com decaimento exponencial.')

    proposicao = models.ForeignKey(
        EtapaProposicao, on_delete=models.CASCADE, related_name='temperatura_historico')

    class Meta:
        ordering = ('-periodo',)
        get_latest_by = '-periodo'


class Comissao(models.Model):
    '''
    Composição das comissões
    '''
    cargo = models.TextField(
        blank=True, null=True,
        help_text='Cargo ocupado pelo parlamentar na comissão')

    id_parlamentar = models.TextField(
        blank=True, null=True,
        help_text='Id do parlamentar'
    )

    partido = models.TextField(
        blank=True, null=True,
        help_text='Partido do parlamentar')

    uf = models.TextField(
        blank=True, null=True,
        help_text='Estado do parlamentar')

    situacao = models.TextField(
        blank=True, null=True,
        help_text='Titular ou suplente')

    nome = models.TextField(
        blank=True, null=True,
        help_text='Nome do parlamentar')

    foto = models.TextField(
        blank=True, null=True,
        help_text='Foto do parlamentar'
    )

    sigla = models.TextField(
        help_text='Sigla da comissão')

    casa = models.TextField(
        help_text='Camara ou Senado')


class PautaHistorico(models.Model):
    '''
    Histórico das pautas de uma proposição
    '''

    data = models.DateField('data')

    semana = models.IntegerField('semana')

    local = models.TextField(blank=True)

    em_pauta = models.NullBooleanField(
        help_text='TRUE se a proposicao estiver em pauta, FALSE caso contrario')

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

    numero = models.IntegerField()

    @property
    def titulo(self):
        '''Título da emenda.'''
        return (self.tipo_documento + ' ' + str(self.numero))

    proposicao = models.ForeignKey(
        EtapaProposicao, on_delete=models.CASCADE, related_name='emendas')

    inteiro_teor = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('-data_apresentacao',)
        get_latest_by = '-data_apresentacao'
