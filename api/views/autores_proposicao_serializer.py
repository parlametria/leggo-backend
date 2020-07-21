from rest_framework import serializers, generics
from api.model.autores_proposicao import AutoresProposicao


class AutoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoresProposicao
        fields = (
            "id_leggo",
            "id_autor_parlametria",
            "id_autor",
            "autor"
        )


class AutoresListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoresProposicao
        fields = (
            "id_leggo",
            "id_autor_parlametria",
            "id_autor",
            "entidade"
        )


class AutoresList(generics.ListAPIView):
    """
    Apresenta lista com todas as entidades
     do Congresso Nacional:
     podem ser parlamentares ou não,
     como Presidência da República e Mesas Diretoras.
    """

    serializer_class = AutoresListSerializer

    def get_queryset(self):
        queryset = AutoresProposicao.objects.all()

        return queryset
