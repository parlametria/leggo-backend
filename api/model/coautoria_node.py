from django.db import models


class CoautoriaNode(models.Model):
    '''
    Nós para criação do grafo de coautorias
    '''
    id_leggo = models.TextField(
        help_text='Id do leggo.')

    id_autor = models.IntegerField(
        help_text='Id do autor.')

    nome = models.TextField(
        help_text='Nome do parlamentar.')

    partido = models.TextField(
        help_text='Partido do parlamentar.')

    uf = models.TextField(
        help_text='Uf do parlamentar.')

    bancada = models.TextField(
        help_text='Bancada do parlamentar.')

    casa_autor = models.TextField(
        null=True,
        help_text='Casa do autor.')

    nome_eleitoral = models.TextField(
        help_text='Nome eleitoral do parlamentar.')

    node_size = models.FloatField(
        help_text='Tamanho do nó'
    )

    id_autor_parlametria = models.IntegerField(
        null=True,
        help_text='Id do autor na plataforma parlametria.')
