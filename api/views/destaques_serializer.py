from rest_framework import serializers, generics
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.model.destaques import Destaques


class DestaquesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destaques
        fields = (
            "id_leggo", "id_ext", "casa", "sigla",
            "criterio_aprovada_em_uma_casa", "fase_global",
            "local", "local_casa", "data_inicio", "data_fim",
            "criterio_parecer_aprovado_comissao",
            "comissoes_aprovadas", "criterio_pressao_alta",
            "maximo_pressao_periodo", "agendas")


class DestaquesList(generics.ListAPIView):

    serializer_class = DestaquesSerializer

    def get_queryset(self):

        return Destaques.objects.all()
