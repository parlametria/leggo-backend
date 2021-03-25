from rest_framework import serializers, generics
from api.model.voto import Voto


class VotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voto
        fields = ("id_votacao", "id_parlamentar_parlametria", "voto")


class VotosByParlamentar(generics.ListAPIView):
    '''
        Retorna os votos de um parlamentar
    '''

    serializer_class = VotoSerializer

    def get_queryset(self):

        id_parlamentar = self.kwargs["id_parlamentar"]

        votos = Voto.objects.all()

        if id_parlamentar:
            votos = votos.filter(
                id_parlamentar_parlametria=id_parlamentar
            )

        return votos


class VotosByVotacao(generics.ListAPIView):
    # Retorna todos os votos de uma votação

    serializer_class = VotoSerializer

    def get_queryset(self):

        id_votacao_arg = self.kwargs["id_votacao"]

        votos = Voto.objects.all()

        if id_votacao_arg:
            votos = votos.filter(
                id_votacao=id_votacao_arg
            )

        return votos
