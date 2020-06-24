from django.db import models


class AnotacaoGeral(models.Model):
    """
    Anotações relacionadas a interesses
    """

    data_criacao = models.DateTimeField(help_text="Data de criação da anotação")

    data_ultima_modificacao = models.DateTimeField(
        help_text="Data de ultima modificação da anotação"
    )

    autor = models.TextField(blank=True, null=True, help_text="Autor da anotação")

    categoria = models.TextField(
        blank=True, null=True, help_text="Categoria da anotação"
    )

    titulo = models.TextField(blank=True, null=True, help_text="Título da anotação")

    anotacao = models.TextField(blank=True, null=True, help_text="Conteúdo da anotação")

    peso = models.IntegerField(help_text="Peso de importância da anotação")

    interesse = models.TextField(help_text="Interesse da Proposição")
