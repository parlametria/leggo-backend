from django.db import models
from api.model.etapa_proposicao import EtapaProposicao
from api.model.entidade import Entidade


class Autoria(models.Model):
    '''
    Autoria dos documentos
    '''
    id_leggo = models.TextField(
        help_text='Id do leggo.')

    id_documento = models.IntegerField(
        help_text='Id do documento.')

    sigla = models.TextField(
        null=True,
        help_text='Sigla do documento.')

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

    autores = models.TextField(
        help_text='Todos autores de um documento.')

    id_principal = models.IntegerField(
        null=True,
        help_text='Id da proposição principal do documento.')

    casa = models.TextField(
        null=True,
        help_text='Casa de origem da proposição principal.')

    id_autor_parlametria = models.IntegerField(
        null=True,
        help_text='Id do autor na plataforma parlametria.')

    casa_autor = models.TextField(
        null=True,
        help_text='Casa do autor do documento.')

    tipo_documento = models.TextField(
        null=True,
        help_text='Tipo geral do documento.')

    tipo_acao = models.TextField(
        null=True,
        help_text='Tipo de ação')

    peso_autor_documento = models.FloatField(
        null=True,
        help_text='Peso do autor no documento')

    etapa_proposicao = models.ForeignKey(
        EtapaProposicao, on_delete=models.CASCADE, related_name='autorias', null=True)

    entidade = models.ForeignKey(
        Entidade, on_delete=models.CASCADE, related_name='entidadeAutoria', null=True)
