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
                'id', openapi.IN_PATH, 'Id da proposição no sistema do Leg.go',
                type=openapi.TYPE_INTEGER),
            openapi.Parameter(
                'interesse', openapi.IN_PATH, 'Nome do interesse-alvo', type=openapi.TYPE_STRING),
            openapi.Parameter(
                'peso', openapi.IN_PATH, 'Se deve retornar apenas as anotações tão ou mais importantes do que este valor', type=openapi.TYPE_INTEGER),
            openapi.Parameter(
                'ultimas_n', openapi.IN_PATH, 'Número máximo de retorno das últimas anotações',
                type=openapi.TYPE_INTEGER)
        ]
    )

    def get_queryset(self):
        '''
        Retorna anotações associadas a uma PL feitas por um interesse
        '''

        interesseArg = self.request.query_params.get('interesse')
        peso = self.request.query_params.get('peso', 100)
        ultimos_n = self.request.query_params.get('ultimas_n', 10)
        id_leggo = self.kwargs['id']

        if not interesseArg:
            interesseArg = 'leggo'

        queryset = Anotacao.objects.filter(
            id_leggo=id_leggo, interesse=interesseArg)
        
        if peso:
            queryset = queryset.order_by('peso', '-data_ultima_modificacao').filter(peso__lte=peso)
        
        if ultimos_n:
            queryset = queryset[:int(ultimos_n)]

        return queryset
