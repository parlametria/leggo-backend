from django.db import models
# from django.db.models import Sum


class Teste(models.Model):

    id_leggo = models.TextField("ID do Leggo", help_text="Id interno do leggo.")

    sigla_camara = models.TextField(
        "Sigla da proposição na Câmara", null=True, blank=True
    )

    sigla_senado = models.TextField(
        "Sigla da proposição no Senado", null=True, blank=True
    )

    @property
    def temperatura_coeficiente(self):
        """
        Calcula coeficiente linear das temperaturas nas últimas 6 semanas.
        """
        print(20 * "8")
        print("Hello")
