from enum import Enum
from django.db import models

urls = {
    'camara': 'http://www.camara.gov.br/proposicoesWeb/fichadetramitacao?idProposicao=',
    'senado': 'https://www25.senado.leg.br/web/atividade/materias/-/materia/'
}


# class ChoiceEnum(Enum):
#     @classmethod
#     def choices(cls):
#         return tuple((i.value, i.name) for i in cls)


class Proposicao(models.Model):

    id_ext = models.IntegerField()

    # casas = ChoiceEnum('Casas', 'camara senado')
    # casa = models.IntegerField(choices=casas.choices())

    # regimes = ChoiceEnum('Regimes', 'ordinario prioridade')
    # regime_tramitacao = models.IntegerField(choices=regimes.choices(), null=True)

    # formas_tramitacao = ChoiceEnum('FormasTramitacao', 'conclusivo plenario')
    # forma_apreciacao = models.IntegerField(
    #     choices=formas_tramitacao.choices(), null=True)

    numero = models.IntegerField()
    sigla_tipo = models.CharField(max_length=3)
    ementa = models.TextField(blank=True)
    justificativa = models.TextField(blank=True)
    data_apresentacao = models.DateField(null=True)

    @property
    def sigla(self):
        return f'{self.sigla_tipo} {self.numero}/{self.ano}'

    @property
    def ano(self):
        return self.data_apresentacao.year

    @property
    def url(self):
        return urls[self.casa] + self.id_ext
