from django.db import models
from api.model.proposicao import Proposicao

class ProposicaApensada(models.Model):
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

    proposicao_apensada = models.ForeignKey(
        Proposicao, on_delete=models.CASCADE, related_name="apensadas"
    )

    proposicao_original = models.ForeignKey(
        Proposicao, on_delete=models.CASCADE, related_name="originais"
    )