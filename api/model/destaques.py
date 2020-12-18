from django.db import models
from api.model.proposicao import Proposicao


class Destaques(models.Model):

    id_leggo = models.TextField(
        help_text='Id interno do leggo.'
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

    proposicao = models.ForeignKey(
        Proposicao, on_delete=models.CASCADE, related_name='destaquesProposicao',
        null=True)
