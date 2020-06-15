from django.db import models
from api.utils.ator import get_nome_partido_uf
from api.model.etapa_proposicao import Proposicao
from api.model.etapa_proposicao import Choices


class Atores(models.Model):
    '''
    Atores de documentos
    '''
    id_leggo = models.IntegerField('Id da proposição principal no leggo.')

    id_ext = models.IntegerField('ID Externo',
                                 help_text='Id externo do sistema da casa.')

    casas = Choices('camara senado')
    casa = models.CharField(
        max_length=6, choices=casas.items(),
        help_text='Casa desta proposição.')

    id_autor = models.FloatField('Id do autor do documento')

    tipo_autor = models.TextField('Tipo do autor')

    nome_autor = models.TextField('Nome do autor do documento')

    partido = models.TextField('Partido do ator')

    uf = models.TextField('Estado do ator')

    bancada = models.TextField('Bancada do ator')

    peso_total_documentos = models.FloatField(
        'Contribuição agregada de um determinado autor em documentos')

    num_documentos = models.IntegerField(
        'Quantidade de documentos apresentada por um determinado autor')

    tipo_generico = models.TextField(
        'Tipo do documento')

    sigla_local = models.TextField(
        'Sigla do local'
    )

    is_important = models.BooleanField(
        'É uma comissão ou plenário'
    )

    id_autor_parlametria = models.IntegerField(
        null=True,
        help_text='Id do autor na plataforma parlametria.')

    casa_autor = models.TextField(
        null=True,
        help_text='Casa do autor do documento.')

    @property
    def sigla_local_formatada(self):
        '''Formata a sigla local para ter a casa'''
        if self.casa == 'camara':
            casa = 'Câmara'
        else:
            casa = 'Senado'

        return self.sigla_local + ' - ' + casa

    @property
    def nome_partido_uf(self):
        '''Nome do parlamentar + partido e UF'''
        return get_nome_partido_uf(self.casa, self.bancada,
                                   self.nome_autor, self.partido, self.uf)

    proposicao = models.ForeignKey(
        Proposicao, on_delete=models.CASCADE, related_name='atores')
