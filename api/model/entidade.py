from django.db import models


class Entidade(models.Model):
    """
    Corresponde ao model de parlamentares e demais entidades do Congresso Nacional.
    """

    legislatura = models.IntegerField(help_text="ID da legislatura da entidade")

    id_entidade = models.IntegerField(
        help_text="ID da entidade (para os parlamentares, é o id nas casas)",
    )

    id_entidade_parlametria = models.IntegerField(
        help_text="ID da entidade na plataforma Parlametria",
    )

    casa = models.TextField(help_text="Casa da entidade.")

    nome = models.TextField(help_text="Nome da entidade")

    sexo = models.TextField(null=True, help_text="Sexo da entidade")

    partido = models.TextField(null=True, help_text="Sigla do partido da entidade")

    uf = models.TextField(null=True, help_text="Sigla da uf da entidade")

    situacao = models.TextField(null=True, help_text="Situação da entidade")

    em_exercicio = models.IntegerField(
        null=True, help_text="Flag se a entidade está em exercício ou não"
    )

    is_parlamentar = models.IntegerField(
        help_text="Flag se a entidade é um parlamentar ou não"
    )
