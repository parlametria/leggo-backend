from django.db import models
from api.model.proposicao import Proposicao


class Destaques(models.Model):

    id_leggo = models.TextField(
        help_text='Id interno do leggo.'
    )

    id_ext = models.IntegerField(
        help_text='Id externo do sistema da casa.'
    )

    casa = models.CharField(
        max_length=6,
        help_text='Casa desta proposição.'
    )

    sigla = models.TextField(
        help_text='Sigla da proposição na Câmara.'
    )

    criterio_aprovada_em_uma_casa = models.BooleanField(
        help_text='Matérias aprovadas em pelo menos uma das casas.'
    )

    fase_global = models.TextField(
        blank=True,
        null=True,
        help_text=''
    )

    local = models.TextField(
        blank=True,
        null=True,
        help_text=''
    )

    local_casa = models.CharField(
        blank=True,
        null=True,
        max_length=6,
        help_text=''
    )

    data_inicio = models.DateTimeField(
        blank=True,
        null=True,
        help_text='Data de início da proposição.'
    )

    data_fim = models.DateTimeField(
        blank=True,
        null=True,
        help_text='Data de finalização da proposição.'
    )

    criterio_avancou_comissoes = models.BooleanField(
        blank=True,
        null=True,
        help_text=''
    )

    ccj_camara = models.BooleanField(
        blank=True,
        null=True,
        help_text=''
    )

    parecer_aprovado_comissao = models.BooleanField(
        blank=True,
        null=True,
        help_text='Matéria com parecer aprovado em pelo menos uma comissão.'
    )

    criterio_pressao_alta = models.BooleanField(
        help_text=''
    )

    maximo_pressao_periodo = models.IntegerField(
        blank=True,
        null=True,
        help_text='Número máximo atingido pela pressão.'
    )

    agendas = models.TextField(
        help_text='Agendas que essa matéria está presente.'
    )
