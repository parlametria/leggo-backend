from rest_framework import serializers, generics
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from api.model.autores_proposicao import AutoresProposicao


class AutoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoresProposicao
        fields = (
            "id_leggo",
            "id_camara",
            "id_senado",
            "id_autor_parlametria",
            "id_autor"
        )


class AutoresList(generics.ListAPIView):
    """
    Apresenta lista com todas as entidades
     do Congresso Nacional:
     podem ser parlamentares ou não,
     como Presidência da República e Mesas Diretoras.
    """

    serializer_class = AutoresSerializer

    def get_queryset(self):
        queryset = AutoresProposicao.objects.all()

        return queryset
