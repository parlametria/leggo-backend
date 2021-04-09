from django.db import models
from api.model.proposicao import Proposicao


class LocalAtualProposicao(models.Model):
    """
    Corresponde ao model com mapeamento dos locais atuais das
    proposições monitoradas pelo Leggo
    """

    id_leggo = models.TextField(help_text="ID interno do Leggo")

    sigla_ultimo_local = models.TextField(
        null=True,
        help_text='Sigla do último local da Proposição')

    casa_ultimo_local = models.TextField(
        null=True,
        help_text='Casa do último local da Proposição')

    nome_ultimo_local = models.TextField(
        null=True,
        help_text='Nome do último local da Proposição')

    data_ultima_situacao = models.DateTimeField(
        null=True,
        help_text='Data da última situação registrada para a proposição')

    tipo_local = models.TextField(
        null=True,
        help_text='Tipo do último local da proposição')

    proposicao = models.ForeignKey(
        Proposicao, on_delete=models.CASCADE, related_name='locaisProposicao', null=True)
