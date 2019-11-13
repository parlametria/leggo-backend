from django.db import models
from api.utils.ator import get_nome_partido_uf
from api.model.etapa_proposicao import EtapaProposicao


class Atores(models.Model):
    '''
    Atores de documentos
    '''

    id_autor = models.FloatField('Id do autor do documento')

    tipo_autor = models.TextField('Tipo do autor')

    nome_autor = models.TextField('Nome do autor do documento')

    partido = models.TextField('Partido do ator')

    uf = models.TextField('Estado do ator')

    bancada = models.TextField('Bancada do ator')

    peso_total_documentos = models.FloatField(
        'Quantidade de documentos feitas por um determinado autor')

    tipo_generico = models.TextField(
        'Tipo do documento')

    sigla_local = models.TextField(
        'Sigla do local'
    )

    is_important = models.BooleanField(
        'É uma comissão ou plenário'
    )

    @property
    def nome_partido_uf(self):
        '''Nome do parlamentar + partido e UF'''
        return get_nome_partido_uf(self.bancada,
                                   self.nome_autor, self.partido, self.uf)

    proposicao = models.ForeignKey(
        EtapaProposicao, on_delete=models.CASCADE, related_name='atores')
