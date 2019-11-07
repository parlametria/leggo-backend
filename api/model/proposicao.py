import time
from django.db import models
from scipy import stats


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
