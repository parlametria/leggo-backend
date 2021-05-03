from django.db import models
from munch import Munch
from api.model.proposicao import Proposicao
from api.model.entidade import Entidade

URLS = {
    "camara": "http://www.camara.gov.br/proposicoesWeb/fichadetramitacao?idProposicao=",
    "senado": "https://www25.senado.leg.br/web/atividade/materias/-/materia/",
}


class Choices(Munch):
    def __init__(self, choices):
        super().__init__({i: i for i in choices.split(" ")})


class EtapaProposicao(models.Model):
    id_leggo = models.TextField("ID Leggo", help_text="Id interno do leggo.")

    id_ext = models.IntegerField(
        "ID Externo", help_text="Id externo do sistema da casa."
    )

    proposicao = models.ForeignKey(
        Proposicao, on_delete=models.CASCADE, related_name="etapas", null=True
    )

    numero = models.IntegerField(
        "Número", help_text="Número da proposição naquele ano e casa."
    )

    sigla_tipo = models.CharField(
        "Sigla do Tipo",
        max_length=3,
        help_text="Sigla do tipo da proposição (PL, PLS etc)",
    )

    data_apresentacao = models.DateField("Data de apresentação")

    casas = Choices("camara senado")
    casa = models.CharField(
        max_length=6, choices=casas.items(), help_text="Casa desta proposição."
    )

    regimes = Choices("ordinario prioridade urgencia")
    regime_tramitacao = models.CharField(
        "Regime de tramitação", max_length=10, choices=regimes.items(), null=True
    )

    formas_apreciacao = Choices("conclusiva plenario")
    forma_apreciacao = models.CharField(
        "Forma de Apreciação",
        max_length=10,
        choices=formas_apreciacao.items(),
        null=True,
    )

    ementa = models.TextField(blank=True)

    justificativa = models.TextField(blank=True)

    palavras_chave = models.TextField(blank=True)

    relator_id = models.IntegerField(blank=True, null=True)

    relator_id_parlametria = models.IntegerField(blank=True, null=True)

    casa_origem = models.TextField(blank=True)

    em_pauta = models.BooleanField(
        help_text="TRUE se a proposicao estará em pauta na semana, FALSE caso contrario",
        null=True
    )

    relatoria = models.ForeignKey(
        Entidade, on_delete=models.SET_NULL, related_name="relatoria", null=True
    )

    status = models.TextField(blank=True, null=True)

    sigla = models.TextField(
        "Sigla da proposição",
        blank=True, null=True,
        help_text="Sigla da proposição",
    )

    class Meta:
        indexes = [
            models.Index(fields=["casa", "id_ext"]),
        ]
        ordering = ("data_apresentacao",)

    @property
    def ano(self):
        return self.data_apresentacao.year

    @property
    def url(self):
        """URL para a página da proposição em sua respectiva casa."""
        return URLS[self.casa] + str(self.id_ext)

    @property
    def resumo_tramitacao(self):
        events = []
        for event in self.tramitacao.all():
            events.append(
                {
                    "data": event.data,
                    "casa": event.etapa_proposicao.casa,
                    "sigla_local": event.sigla_local,
                    "local": event.local,
                    "evento": event.evento,
                    "texto_tramitacao": event.texto_tramitacao,
                    "link_inteiro_teor": event.link_inteiro_teor,
                }
            )
        return sorted(events, key=lambda k: k["data"])

    @property
    def top_resumo_tramitacao(self):
        return self.resumo_tramitacao[:3]

    @property
    def comissoes_passadas(self):
        """
        Pega todas as comissões nas quais a proposição já
        tramitou
        """
        comissoes = set()
        local_com_c_que_nao_e_comissao = "CD-MESA-PLEN"
        for row in self.tramitacao.values("local"):
            if (
                row["local"] != local_com_c_que_nao_e_comissao
                and row["local"][0] == "C"
            ):
                comissoes.add(row["local"])
        return comissoes
