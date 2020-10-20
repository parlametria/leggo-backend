from django.db import models
from api.model.proposicao import Proposicao
from api.model.entidade import Entidade


class RelatoresProposicao(models.Model):
    """
    Corresponde ao model de relatores das proposições monitoradas pelo Leggo
    """

    id_leggo = models.TextField(help_text="ID interno do Leggo")

    id_ext = models.IntegerField(
        help_text="Id externo da etapa da proposição na qual o parlamentar foi relator",
        null=True,
        blank=True,
        default=None
    )

    casa = models.TextField(
        null=True,
        help_text='Casa da etapa da proposição')

    relator_id = models.IntegerField(help_text="Id do relator na casa de origem")

    relator_id_parlametria = models.IntegerField(
        help_text="Id do autor no Parlametria")

    relator_nome = models.TextField(
        null=True,
        help_text='Casa da etapa da proposição')

    proposicao = models.ForeignKey(
        Proposicao, on_delete=models.CASCADE,
        related_name='relatoresProposicao', null=True)

    entidade = models.ForeignKey(
        Entidade, on_delete=models.CASCADE, related_name='entidadeRelator', null=True)
