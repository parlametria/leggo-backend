from rest_framework import serializers, generics
from api.model.voto import Voto


class VotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voto
        fields = ("id_votacao", "id_parlamentar_parlametria", "voto")


class VotosByParlamentar(generics.ListAPIView):
    '''
    Retorna todas as votaões
    '''

    serializer_class = VotoSerializer

    def get_queryset(self):
        '''
        Retorna as votações de uma casa
        '''

        id_parlamentar = self.kwargs["id_parlamentar"]

        votos = Voto.objects().all()

        if id_parlamentar:
            votos = votos.filter(
                id_parlamentar_parlametria=id_parlamentar
            )

        return votos
