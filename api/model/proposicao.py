import time
from django.db import models
from scipy import stats
from django.db.models import Sum
from api.utils.ator import get_nome_partido_uf


ORDER_PROGRESSO = [
    ('Construção', 'Comissões'),
    ('Construção', 'Plenário'),
    ('Revisão I', 'Comissões'),
    ('Revisão I', 'Plenário'),
    ('Revisão II', 'Comissões'),
    ('Revisão II', 'Plenário'),
    ('Promulgação/Veto', 'Presidência da República'),
    ('Sanção/Veto', 'Presidência da República'),
    ('Avaliação dos Vetos', 'Congresso'),
]

ORDER_PROGRESSO_MPV = [
    ("Comissão Mista"),
    ("Câmara dos Deputados"),
    ("Senado Federal"),
    ("Câmara dos Deputados - Revisão"),
    ("Sanção Presidencial/Promulgação")
]


class Proposicao(models.Model):

    apelido = models.TextField(blank=True)
    tema = models.TextField(blank=True)
    id_leggo = models.IntegerField(
        'ID do Leggo',
        help_text='Id interno do leggo.')

    @property
    def resumo_progresso(self):
        if self.progresso.filter(fase_global='Comissão Mista').exists():
            return sorted(
                [{
                    'fase_global': progresso.fase_global,
                    'local': progresso.local,
                    'data_inicio': progresso.data_inicio,
                    'data_fim': progresso.data_fim,
                    'local_casa': progresso.local_casa,
                    'is_mpv': True,
                    'pulou': progresso.pulou
                } for progresso in self.progresso.exclude(fase_global__icontains='Pré')],
                key=lambda x: ORDER_PROGRESSO_MPV.index((x['fase_global'])))
        else:
            return sorted(
                [{
                    'fase_global': progresso.fase_global,
                    'local': progresso.local,
                    'data_inicio': progresso.data_inicio,
                    'data_fim': progresso.data_fim,
                    'local_casa': progresso.local_casa,
                    'is_mpv': False,
                    'pulou': progresso.pulou
                } for progresso in self.progresso.exclude(fase_global__icontains='Pré')],
                key=lambda x: ORDER_PROGRESSO.index((x['fase_global'], x['local'])))

    @property
    def temperatura_coeficiente(self):
        '''
        Calcula coeficiente linear das temperaturas nas últimas 6 semanas.
        '''
        temperatures = self.temperatura_historico.values(
            'periodo', 'temperatura_recente')[:6]
        dates_x = [
            time.mktime(temperatura['periodo'].timetuple())
            for temperatura in temperatures]
        temperaturas_y = [
            temperatura['temperatura_recente']
            for temperatura in temperatures]

        if (dates_x and temperaturas_y and len(dates_x) > 1 and len(temperaturas_y) > 1):
            return stats.linregress(dates_x, temperaturas_y)[0]
        else:
            return 0

    @property
    def ultima_temperatura(self):
        temperaturas = self.temperatura_historico.values('temperatura_recente')
        if (len(temperaturas) == 0):
            return 0
        else:
            return temperaturas[0]['temperatura_recente']

    @property
    def temas(self):
        '''
        Separa temas
        '''
        return self.tema.split(";")
    
    @property
    def top_atores(self):
        '''
        Retorna os top 15 atores (caso tenha menos de 15 retorna todos)
        '''
        atores_filtrados = []

        top_n_atores = self.atores.values('id_autor') \
            .annotate(total_docs=Sum('peso_total_documentos')) \
            .order_by('-total_docs')[:15]
        atores_por_tipo_gen = self.atores.values('id_autor', 'nome_autor', 'uf',
                                                 'partido', 'tipo_generico', 
                                                 'bancada', 'casa') \
            .annotate(total_docs=Sum('peso_total_documentos'))

        for ator in atores_por_tipo_gen:
            for top_n_ator in top_n_atores:
                if ator['id_autor'] == top_n_ator['id_autor']:
                    atores_filtrados.append({
                        'id_autor': ator['id_autor'],
                        'peso_total_documentos': ator['total_docs'],
                        'tipo_generico': ator['tipo_generico'],
                        'bancada': ator['bancada'],
                        'casa': ator['casa'],
                        'nome_partido_uf': get_nome_partido_uf(
                            ator['casa'], ator['bancada'], ator['nome_autor'],
                            ator['partido'], ator['uf'])
                    })

        return atores_filtrados

    @property
    def top_important_atores(self):
        '''
        Retorna os atores por local (apenas locais importantes:
        comissões e plenário)
        '''
        atores_filtrados = []

        top_n_atores = self.atores.values('id_autor') \
            .annotate(total_docs=Sum('peso_total_documentos')) \
            .order_by('-total_docs')
        for ator in self.atores.all():
            for top_n_ator in top_n_atores:
                if ator.id_autor == top_n_ator['id_autor'] and ator.is_important:
                    atores_filtrados.append({
                        'id_autor': ator.id_autor,
                        'nome_autor': ator.nome_autor,
                        'peso_total_documentos': ator.peso_total_documentos,
                        'uf': ator.uf,
                        'casa': ator.casa,
                        'partido': ator.partido,
                        'tipo_generico': ator.tipo_generico,
                        'bancada': ator.bancada,
                        'nome_partido_uf': ator.nome_partido_uf,
                        'sigla_local_formatada': ator.sigla_local_formatada,
                        'is_important': ator.is_important
                    })

        return atores_filtrados
