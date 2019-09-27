from django.db import models

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
    advocacy_link = models.TextField(blank=True)

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
    def temas(self):
        '''
        Separa temas
        '''
        return self.tema.split(";")