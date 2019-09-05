from django.db import models


class Comissao(models.Model):
    '''
    Composição das comissões
    '''
    cargo = models.TextField(
        blank=True, null=True,
        help_text='Cargo ocupado pelo parlamentar na comissão')

    id_parlamentar = models.TextField(
        blank=True, null=True,
        help_text='Id do parlamentar'
    )

    partido = models.TextField(
        blank=True, null=True,
        help_text='Partido do parlamentar')

    uf = models.TextField(
        blank=True, null=True,
        help_text='Estado do parlamentar')

    situacao = models.TextField(
        blank=True, null=True,
        help_text='Titular ou suplente')

    nome = models.TextField(
        blank=True, null=True,
        help_text='Nome do parlamentar')

    foto = models.TextField(
        blank=True, null=True,
        help_text='Foto do parlamentar'
    )

    sigla = models.TextField(
        help_text='Sigla da comissão')

    casa = models.TextField(
        help_text='Camara ou Senado')
