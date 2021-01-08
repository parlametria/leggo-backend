from rest_framework import serializers
from api.model.destaques import Destaques


class DestaquesDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Destaques
        fields = (
            "id_leggo", "casa_origem", "casa_revisora",
            "criterio_aprovada_em_uma_casa", "casa_aprovacao",
            "data_aprovacao", "criterio_avancou_comissoes",
            "comissoes_camara", "comissoes_senado",
            "criterio_req_urgencia_apresentado", "casa_req_urgencia_apresentado",
            "data_req_urgencia_apresentado", "criterio_req_urgencia_aprovado",
            "casa_req_urgencia_aprovado", "data_req_urgencia_aprovado")
