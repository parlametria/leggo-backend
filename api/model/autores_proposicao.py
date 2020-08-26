from django.db import models
from api.model.proposicao import Proposicao
from api.model.entidade import Entidade


class AutoresProposicao(models.Model):
    """
    Corresponde ao model de autores das proposições monitoradas pelo Leggo
    """

    id_leggo = models.TextField(help_text="ID interno do Leggo")

    id_camara = models.IntegerField(
        help_text="Id externo do sistema da Câmara",
        null=True,
        blank=True,
        default=None
    )

    id_senado = models.IntegerField(
        help_text="Id externo do sistema do Senado",
        null=True,
        blank=True,
        default=None
    )

    id_autor_parlametria = models.IntegerField(help_text="Id do autor no Parlametria")

    id_autor = models.IntegerField(help_text="Id do autor na casa de origem.")

    proposicao = models.ForeignKey(
        Proposicao, on_delete=models.CASCADE, related_name='autoresProposicao', null=True)

    entidade = models.ForeignKey(
        Entidade, on_delete=models.CASCADE, related_name='entidadeAutor', null=True)

    @property
    def autor(self):
        infoAutor = {
            "nome": self.entidade.nome,
            "uf": self.entidade.uf,
            "partido": self.entidade.partido,
            "is_parlamentar": self.entidade.is_parlamentar,
            "casa": self.entidade.casa
        }
        return infoAutor
