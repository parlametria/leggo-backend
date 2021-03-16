from django.db import models
from api.model.entidade import Entidade


class Disciplina(models.Model):
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

    disciplina = models.FloatField(
        null=True,
        help_text='Valor do disciplina')

    entidade = models.ForeignKey(
        Entidade, on_delete=models.CASCADE, related_name='entidadeDisciplina', null=True)
