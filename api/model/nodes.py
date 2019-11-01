from django.db import models


class Nodes(models.Model):
    '''
    Nós para criação do grafo de coautorias
    '''
    id_leggo = models.IntegerField(
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

    nome_eleitoral = models.TextField(
        help_text='Nome eleitoral do parlamentar.')

    node_size = models.FloatField(
        help_text='Tamanho do nó'
    )
