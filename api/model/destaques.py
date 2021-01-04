from django.db import models
from api.model.proposicao import Proposicao


class Destaques(models.Model):

    id_leggo = models.TextField(
        help_text='Id interno do leggo.'
    )

    casa_origem = models.CharField(
        blank=True,
        null=True,
        max_length=6,
        help_text='Casa de origem da proposição'
    )

    casa_revisora = models.CharField(
        blank=True,
        null=True,
        max_length=6,
        help_text='Casa revisora da proposição'
    )

    criterio_aprovada_em_uma_casa = models.BooleanField(
        blank=True,
        null=True,
        help_text='Matérias aprovadas em pelo menos uma das casas.'
    )

    casa_aprovacao = models.CharField(
        blank=True,
        null=True,
        max_length=6,
        help_text=''
    )

    data_aprovacao = models.DateTimeField(
        blank=True,
        null=True,
        help_text='Data de finalização da proposição.'
    )

    criterio_avancou_comissoes = models.BooleanField(
        blank=True,
        null=True,
        help_text=''
    )

    comissoes_camara = models.TextField(
        blank=True,
        null=True,
        help_text=''
    )

    comissoes_senado = models.TextField(
        blank=True,
        null=True,
        help_text=''
    )

    criterio_req_urgencia_apresentado = models.BooleanField(
        blank=True,
        null=True,
        help_text='Matérias com requerimento de urgência apresentado.'
    )

    casa_req_urgencia_apresentado = models.TextField(
        blank=True,
        null=True,
        help_text=''
    )

    data_req_urgencia_apresentado = models.DateTimeField(
        blank=True,
        null=True,
        help_text='Data de de apresentação do requerimento de urgência.'
    )

    criterio_req_urgencia_aprovado = models.BooleanField(
        blank=True,
        null=True,
        help_text='Matérias com requerimento de urgência aprovado.'
    )

    casa_req_urgencia_aprovado = models.TextField(
        blank=True,
        null=True,
        help_text=''
    )

    data_req_urgencia_aprovado = models.DateTimeField(
        blank=True,
        null=True,
        help_text='Data de de aprovação do requerimento de urgência'
    )

    proposicao = models.ForeignKey(
        Proposicao, on_delete=models.CASCADE, related_name="destaques",
        blank=True,
        null=True
    )
