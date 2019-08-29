from django.db import models
from api.model.proposicao import Proposicao
class Progresso(models.Model):

    local_casa = models.CharField(
        max_length=30,
        help_text='Casa desta proposição.',
        null=True)

    fase_global = models.TextField(blank=True)

    local = models.TextField(blank=True, null=True)

    data_inicio = models.DateField('Data de início', null=True, blank=True)

    data_fim = models.DateField('Data final', null=True, blank=True)

    proposicao = models.ForeignKey(
        Proposicao, on_delete=models.CASCADE, related_name='progresso')

    pulou = models.NullBooleanField(
        help_text='TRUE se a proposicao pulou a fase, FALSE caso contrario')
