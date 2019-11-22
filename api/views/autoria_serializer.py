from rest_framework import serializers, generics
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from api.model.autoria import Autoria


class AutoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autoria
        fields = (
            'id_leggo', 'id_documento', 'id_autor',
            'descricao_tipo_documento', 'data',
            'url_inteiro_teor', 'nome_eleitoral')


class AutoriaList(generics.ListAPIView):
    '''
    Dados de autoria de uma proposição
    '''

    serializer_class = AutoriaSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'id', openapi.IN_PATH, 'id da proposição no sistema do Leg.go',
                type=openapi.TYPE_INTEGER),
        ]
    )
    def get_queryset(self):
        '''
        Retorna a autoria
        '''
        id_prop = self.kwargs['id']
        return Autoria.objects.filter(id_leggo=id_prop)
