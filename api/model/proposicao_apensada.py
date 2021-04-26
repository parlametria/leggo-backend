from django.db import models
from api.model.proposicao import Proposicao


class ProposicaoApensada(models.Model):
    id_leggo = models.TextField(
        'ID do Leggo',
        help_text='Id interno do leggo.'
    )

    id_leggo_prop_principal = models.TextField(
        'ID do Leggo',
        help_text='Id interno do leggo da proposição original.',
        null=True,
        blank=True
    )

    id_ext_prop_principal = models.IntegerField(
        'Id externo da proposição original na API da Câmara ou Senado',
        null=True,
        blank=True
    )

    casa_prop_principal = models.TextField(
       'Casa da proposição original onde houve a apensação',
       null=True,
       blank=True
    )

    interesse = models.TextField(
       'Interesse das proposições',
       null=True,
       blank=True
    )

    proposicao = models.ForeignKey(
        Proposicao, on_delete=models.CASCADE, related_name="apensadas"
    )

    proposicao_principal = models.ForeignKey(
        Proposicao, on_delete=models.CASCADE, related_name="principal",
        null=True,
        blank=True
    )
