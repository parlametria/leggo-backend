from django.db import models
from api.model.proposicao import Proposicao


class Votacao(models.Model):

    id_leggo = models.TextField(
        help_text='Id interno do leggo.',
        null=True,
        blank=True
    )

    id_votacao = models.TextField(
        help_text='Id da votação nas APIs.'
    )

    data = models.DateField(
        blank=True,
        null=True,
        help_text='Data da votação.'
    )

    obj_votacao = models.TextField(
        help_text='Objeto de votação.'
    )

    casa = models.TextField(
        help_text='Casa.'
    )

    resumo = models.TextField(
        help_text='Resumo da votação.'
    )

    is_nominal = models.BooleanField(
        help_text='Flag se a votação é nominal.',
        null=True)

    proposicao = models.ForeignKey(
        Proposicao, on_delete=models.CASCADE, related_name="votacoes",
        blank=True,
        null=True
    )
