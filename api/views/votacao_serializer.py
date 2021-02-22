from rest_framework import serializers, generics
from api.model.votacao import Votacao


class VotacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Votacao
        fields = ("id_leggo", "casa", "data", "id_votacao", "obj_votacao", "resumo")


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
        if not casaArg:
            casaArg = "camara"

        queryset = (
            Votacao.objects.filter(
                casa=casaArg)
        )

        return queryset
