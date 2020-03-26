from django.db import models
from api.model.proposicao import Proposicao


class Interesse(models.Model):
    '''
    Interesses analisados e relacionados as PL's
    '''

    id_leggo = models.IntegerField(
        help_text='Id da proposição no Leggo.')

    interesse = models.TextField(
        help_text='Interesse da Proposição')

    apelido = models.TextField(
        help_text='Apelido da Proposição')

    tema = models.TextField(
        help_text='Temas da Proposição')

    keywords = models.TextField(
        help_text='Conjunto de palavras-chave da Proposição')

    advocacy_link = models.TextField(
        help_text='Link para conteúdo advocacy da Proposição')

    tipo_agenda = models.TextField(
        help_text='Tipo da Agenda da Proposição')

    proposicao = models.ForeignKey(
        Proposicao, on_delete=models.CASCADE, related_name='interesse')

    @property
    def temas(self):
        '''
        Separa temas
        '''
        return self.tema.split(";")
