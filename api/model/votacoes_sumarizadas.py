from django.db import models
from api.model.entidade import Entidade


class VotacoesSumarizadas(models.Model):

    '''
    Disciplina dos parlamentares em votações
    '''

    id_parlamentar = models.IntegerField(
        null=True,
        help_text='Id do parlamentar')

    id_parlamentar_parlametria = models.IntegerField(
        null=True,
        help_text='Id do parlamentar na plataforma parlametria')

    casa = models.TextField(
        null=True,
        help_text='Casa do parlamentar')

    num_votacoes_parlamentar_disciplina = models.IntegerField(
        null=True,
        help_text='Número de votações do parlamentar')

    num_votacoes_parlamentar_governismo = models.IntegerField(
        null=True,
        help_text='Número de votações do parlamentar')

    num_votacoes_totais_disciplina = models.IntegerField(
        null=True,
        help_text='Número de votações totais')

    num_votacoes_totais_governismo = models.IntegerField(
        null=True,
        help_text='Número de votações totais')

    entidade = models.ForeignKey(
        Entidade, on_delete=models.CASCADE,
        related_name='entidadeVotacoesSumarizadas',
        null=True)
