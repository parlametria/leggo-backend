from django.db import models
from api.model.proposicao import Proposicao


class Interesse(models.Model):
    """
    Interesses analisados e relacionados as PL's
    """

    id_leggo = models.TextField(help_text="Id da proposição no Leggo.")

    interesse = models.TextField(
        blank=True, null=True, help_text="Interesse da Proposição"
    )

    apelido = models.TextField(blank=True, null=True, help_text="Apelido da Proposição")

    tema = models.TextField(blank=True, null=True, help_text="Temas da Proposição")

    tema_slug = models.TextField(
        blank=True, null=True, help_text="Slug dos temas da Proposição"
    )

    keywords = models.TextField(
        blank=True, null=True, help_text="Conjunto de palavras-chave da Proposição"
    )

    advocacy_link = models.TextField(
        blank=True, null=True, help_text="Link para conteúdo advocacy"
    )

    tipo_agenda = models.TextField(
        blank=True, null=True, help_text="Tipo da Agenda da Proposição"
    )

    proposicao = models.ForeignKey(
        Proposicao, on_delete=models.CASCADE, related_name="interesse"
    )

    nome_interesse = models.TextField(
        blank=True, null=True, help_text="Nome do Interesse da Proposição"
    )

    @property
    def temas(self):
        """
        Separa temas
        """
        return self.tema.split(";")

    @property
    def slug_temas(self):
        """
        Separa temas
        """
        return self.tema_slug.split(";")

    @property
    def ultima_pressao(self):
        pressoes = []
        for p in self.pressaoInteresse.values("trends_max_popularity", "date"):
            pressoes.append(
                {"maximo_geral": p["trends_max_popularity"], "date": p["date"]}
            )

        if len(pressoes) == 0:
            return -1
        else:
            sorted_pressoes = sorted(pressoes, key=lambda k: k["date"], reverse=True)
            return sorted_pressoes[0]["maximo_geral"]

    @property
    def obj_temas(self):
        obj = []
        for i in range(len(self.temas)):
            data = {"tema": self.temas[i], "tema_slug": self.slug_temas[i]}
            obj.append(data)

        return obj
