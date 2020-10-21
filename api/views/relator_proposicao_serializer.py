from rest_framework import serializers, generics
from api.model.relatores_proposicao import RelatoresProposicao
from api.utils.filters import get_filtered_interesses


class RelatoresListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatoresProposicao
        fields = (
            "id_leggo",
            "id_ext",
            "casa",
            "relator_id",
            "relator_id_parlametria",
            "relator_nome"
        )


class RelatoresList(generics.ListAPIView):
    """
    Apresenta lsita de relatores das proposições monitoradas
    """

    serializer_class = RelatoresListSerializer

    def get_queryset(self):
        interesse_arg = self.request.query_params.get('interesse')
        tema_arg = self.request.query_params.get('tema')
        if interesse_arg is None:
            interesse_arg = 'leggo'
        interesses = get_filtered_interesses(interesse_arg, tema_arg)

        queryset = (
            RelatoresProposicao.objects
            .filter(id_leggo__in=interesses.values('id_leggo'))
            .values("id_leggo",
                    "id_ext",
                    "casa",
                    "relator_id",
                    "relator_id_parlametria",
                    "relator_nome")
        )

        return queryset
