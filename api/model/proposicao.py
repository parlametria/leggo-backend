import time
from django.db import models
from scipy import stats
from django.db.models import Sum


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

    id_leggo = models.TextField(
        'ID do Leggo',
        help_text='Id interno do leggo.')

    sigla_camara = models.TextField(
        'Sigla da proposição na Câmara',
        null=True,
        blank=True
    )

    sigla_senado = models.TextField(
        'Sigla da proposição no Senado',
        null=True,
        blank=True
    )

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
    def important_atores(self):
        '''
        Retorna os atores por local (apenas locais importantes:
        comissões e plenário)
        '''
        top_n_atores = self.atores.values('id_autor') \
            .annotate(total_docs=Sum('peso_total_documentos')) \
            .order_by('-total_docs') \
            .values('id_autor')

        atores = self.atores.filter(id_autor__in=top_n_atores) \
            .select_related("entidade") \
            .values(
                "id_autor",
                "id_autor_parlametria",
                "tipo_generico",
                "sigla_local",
                "tipo_autor",
                "casa_autor",
                "bancada",
                "is_important",
                "num_documentos",
                "peso_total_documentos",
                "entidade__nome",
                "entidade__uf",
                "entidade__partido"
            )
        return atores

    @property
    def anotacao_data_ultima_modificacao(self):
        datas_anotacoes = self.anotacao.values('data_ultima_modificacao')
        len_datas_anotacoes = len(datas_anotacoes)
        if (len_datas_anotacoes == 0):
            return None
        else:
            return datas_anotacoes[len_datas_anotacoes - 1]['data_ultima_modificacao']
