from django.db import models


class Autoria(models.Model):
    '''
    Autoria dos documentos
    '''
    id_leggo = models.IntegerField(
        help_text='Id do leggo.')

    id_documento = models.IntegerField(
        help_text='Id do documento.')

    descricao_tipo_documento = models.TextField(
        help_text='Tipo do documento.')

    id_autor = models.IntegerField(
        help_text='Id do autor.')

    data = models.DateField(
        help_text='Data do documento.')

    url_inteiro_teor = models.TextField(
        help_text='URL do documento.')

    nome_eleitoral = models.TextField(
        help_text='Nome eleitoral do parlamentar.')
