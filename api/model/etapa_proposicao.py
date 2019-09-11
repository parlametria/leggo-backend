import time
from django.db import models
from munch import Munch
from api.model.proposicao import Proposicao
from django.db.models import Sum
from scipy import stats
from api.utils.ator import get_nome_partido_uf

URLS = {
    'camara': 'http://www.camara.gov.br/proposicoesWeb/fichadetramitacao?idProposicao=',
    'senado': 'https://www25.senado.leg.br/web/atividade/materias/-/materia/'
}


class Choices(Munch):
    def __init__(self, choices):
        super().__init__({i: i for i in choices.split(' ')})


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
        '''
        Retorna autores das pls de acordo com partido e UF
        '''
        nomes = self.autor_nome.split('+')
        partidos = self.autor_partido.split('+')
        ufs = self.autor_uf.split('+')

        autores = []
        presidencia = ['Poder Executivo', 'Presidência', 'Câmara dos Deputados']
        for i in range(len(nomes)):
            autor = nomes[i].strip()
            if autor in presidencia:
                autores.append(autor)
            elif 'Senado Federal' in autor:
                senado = autor.split(' - ')
                if 'Comissão' in senado[-1]:
                    autores.append(senado[-1])
                else:
                    autores.append('Sen. ' + senado[-1])
            elif 'Legislação' in autor:
                autores.append('Câm. ' + autor)
            elif self.casa_origem == 'senado':
                autores.append('Sen. ' + autor)
            else:
                if self.casa == 'senado':
                    autores.append('Dep. ' + autor)
                else:
                    autores.append('Dep. ' +
                                   autor + ' (' + partidos[i] + '-' + ufs[i] + ')')
        return autores

    @property
    def temas(self):
        '''
        Separa temas
        '''
        return self.tema.split(";")

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
    def ultima_temperatura(self):
        if (len(self.temperatura_historico.all()) == 0):
            return 0
        else:
            return self.temperatura_historico.all()[0].temperatura_recente

    @property
    def top_atores(self):
        '''
        Retorna os top 15 atores (caso tenha menos de 15 retorna todos)
        '''
        atores_filtrados = []

        top_n_atores = self.atores.values('id_autor') \
            .annotate(total_docs=Sum('qtd_de_documentos')) \
            .order_by('-total_docs')[:15]
        atores_por_tipo_gen = self.atores.values('id_autor', 'nome_autor', 'uf',
                                                 'partido', 'tipo_generico') \
            .annotate(total_docs=Sum('qtd_de_documentos'))

        for ator in atores_por_tipo_gen:
            for top_n_ator in top_n_atores:
                if ator['id_autor'] == top_n_ator['id_autor']:
                    atores_filtrados.append({
                        'id_autor': ator['id_autor'],
                        'qtd_de_documentos': ator['total_docs'],
                        'tipo_generico': ator['tipo_generico'],
                        'nome_partido_uf': get_nome_partido_uf(
                            ator['nome_autor'], ator['partido'], ator['uf'])
                    })

        return atores_filtrados

    @property
    def top_important_atores(self):
        '''
        Retorna os atores e comissões e plenário
        '''
        atores_filtrados = []

        top_n_atores = self.atores.values('id_autor') \
            .annotate(total_docs=Sum('qtd_de_documentos')) \
            .order_by('-total_docs')
        for ator in self.atores.all():
            for top_n_ator in top_n_atores:
                if ator.id_autor == top_n_ator['id_autor'] and ator.is_important:
                    atores_filtrados.append({
                        'id_autor': ator.id_autor,
                        'nome_autor': ator.nome_autor,
                        'qtd_de_documentos': ator.qtd_de_documentos,
                        'uf': ator.uf,
                        'partido': ator.partido,
                        'tipo_generico': ator.tipo_generico,
                        'nome_partido_uf': ator.nome_partido_uf,
                        'sigla_local': ator.sigla_local,
                        'is_important': ator.is_important
                    })

        return atores_filtrados

    @property
    def status(self):
        # It's pefetched, avoid query
        status_list = ['Caducou', 'Rejeitada', 'Lei']
        trams = list(self.tramitacao.all())
        if trams:
            for tram in trams:
                if (tram.status in status_list):
                    return tram.status
            return trams[-1].status
        else:
            return None

    @property
    def resumo_tramitacao(self):
        events = []
        for event in self.tramitacao.all():
            events.append({
                'data': event.data,
                'casa': event.etapa_proposicao.casa,
                'sigla_local': event.sigla_local,
                'local': event.local,
                'evento': event.evento,
                'texto_tramitacao': event.texto_tramitacao,
                'link_inteiro_teor': event.link_inteiro_teor
            })
        return sorted(events, key=lambda k: k['data'])

    @property
    def top_resumo_tramitacao(self):
        return self.resumo_tramitacao[:3]

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

    @property
    def ultima_pressao(self):
        pressoes = []
        for p in self.pressao.all():
            pressoes.append({
                'maximo_geral': p.maximo_geral,
                'date': p.date
            })

        if (len(pressoes) == 0):
            return -1
        else:
            sorted_pressoes = sorted(pressoes, key=lambda k: k['date'], reverse=True)
            return sorted_pressoes[0]['maximo_geral']
