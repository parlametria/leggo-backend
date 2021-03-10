from django.db import models
from api.model.entidade import Entidade
from api.model.votacao import Votacao


class Voto(models.Model):

    id_parlamentar = models.IntegerField(
        null=True,
        help_text='Id do parlamentar.'
    )

    id_parlamentar_parlametria = models.IntegerField(
        null=True,
        help_text='Id do parlamentar na plataforma parlametria.'
    )

    id_votacao = models.TextField(
        help_text='Id da votação nas APIs.'
    )

    partido = models.TextField(
        help_text='Partido do parlamentar.'
    )

    voto = models.TextField(
        help_text='Voto do parlamentar.'
    )

    casa = models.TextField(
        help_text='Casa do parlamentar.'
    )

    entidade = models.ForeignKey(
        Entidade, on_delete=models.CASCADE, related_name="votoEntidade",
        blank=True,
        null=True
    )

    votacao = models.ForeignKey(
        Votacao, on_delete=models.CASCADE, related_name="votoVotacao",
        blank=True,
        null=True
    )
