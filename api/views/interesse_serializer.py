from rest_framework import serializers, generics
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from api.model.interesse import Interesse


class InteresseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interesse
        fields = (
            'interesse', 'nome_interesse', 'temas', 'apelido', 'advocacy_link',
            'tipo_agenda', 'ultima_pressao')


class InteresseList(generics.ListAPIView):
    '''
    Apresenta lista com mapeamento entre as proposições analisadas e os
    interesses abordados pelo Leggo. Um interesse é um assunto geral
    no qual um conjunto de proposições está relacionado. O primeiro
    interesse analisado pelo Leggo é o da RAC, que é uma rede de
    organizações que atua no Congresso em diferentes eixos como
    Meio Ambiente, Direitos Humanos, Nova Economia e Transparência.
    Outros possíveis interesses seriam Primeira Infância (conjunto
    de proposições ligadas a direitos e deveres relacionados às
    crianças).
    '''

    serializer_class = InteresseSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'id', openapi.IN_PATH, 'id da proposição no sistema do Leg.go',
                type=openapi.TYPE_INTEGER),
        ]
    )
    def get_queryset(self):
        '''
        Retorna interesses associados a uma PL
        '''
        id_prop = self.kwargs['id']
        return Interesse.objects.filter(id_leggo=id_prop)


class TemaSerializer(serializers.Serializer):
    temas = serializers.ListField()


class TemaList(generics.ListAPIView):
    """
    Retorna lista de temas associados a uma agenda.
    """

    serializer_class = TemaSerializer

    def get_queryset(self):

        temas = []

        interesse_arg = self.request.query_params.get("interesse")
        if interesse_arg is None:
            interesse_arg = 'leggo'

        [
            temas.extend(list(set(i.temas) - set(temas))) 
            for i in Interesse.objects.filter(interesse=interesse_arg).distinct('tema')
        ]

        queryset = [
            {
                'temas': temas
            }
        ]

        return queryset
