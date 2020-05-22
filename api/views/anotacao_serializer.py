from rest_framework import serializers, generics
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from api.model.anotacao import Anotacao


class AnotacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anotacao
        fields = (
            'id_leggo', 'interesse', 'data_criacao', 'data_ultima_modificacao', 'autor', 'titulo',
            'anotacao', 'peso')


class AnotacaoList(generics.ListAPIView):
    '''
    Apresenta uma lista com as anotações feitas sobre as proposições por
    interesses abordados pelo Leggo. As anotações são compostas por data de
    criação e última modificação, autor, titulo, conteúdo, peso de importância e
    interesse relacionado.
    '''

    serializer_class = AnotacaoSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'id', openapi.IN_PATH, 'id da proposição no sistema do Leg.go',
                type=openapi.TYPE_INTEGER),
        ]
    )

    def get_queryset(self):
        '''
        Retorna anotações associadas a uma PL feitas por um interesse
        '''

        interesseArg = self.request.query_params.get('interesse')

        # Adiciona interesse default
        if interesseArg is None:
            interesseArg = 'leggo'

        id_leggo = self.kwargs['id']
        queryset = Anotacao.objects.filter(
            id_leggo=id_leggo, interesse=interesseArg)

        return queryset
