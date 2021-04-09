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

    partido_atual = models.TextField(
        null=True,
        help_text='Partido atual do parlamentar'
    )

    partido_disciplina = models.TextField(
        null=True,
        help_text='Partido da disciplina'
    )

    casa = models.TextField(
        null=True,
        help_text='Casa do parlamentar')

    disciplina = models.FloatField(
        null=True,
        help_text='Valor do disciplina')

    bancada_suficiente = models.BooleanField(
        null=True,
        help_text='Se o partido tem bancada suficiente'
    )

    entidade = models.ForeignKey(
        Entidade, on_delete=models.CASCADE, related_name='entidadeDisciplina', null=True)
