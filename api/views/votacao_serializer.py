from rest_framework import serializers, generics
from api.model.votacao import Votacao


class VotacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Votacao
        fields = (
            "id_leggo",
            "casa",
            "data",
            "id_votacao",
            "obj_votacao",
            "resumo",
            "is_nominal"
        )


class VotacoesByCasaList(generics.ListAPIView):
    '''
    Retorna todas as votaões
    '''

    serializer_class = VotacaoSerializer

    def get_queryset(self):
        '''
        Retorna as votações de uma casa
        '''

        casaArg = self.request.query_params.get("casa")
        isNominalArg = self.request.query_params.get("nominal")

        if not casaArg:
            casaArg = "camara"

        if not isNominalArg or isNominalArg == 'true':
            isNominalArg = True
        else:
            isNominalArg = False

        queryset = (
            Votacao.objects.filter(
                casa=casaArg,
                is_nominal=isNominalArg)
        )

        return queryset
