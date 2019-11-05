from rest_framework import serializers, generics
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.model.coautoria_node import CoautoriaNode


class CoautoriaNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoautoriaNode
        fields = ('id_autor', 'nome', 'partido', 'uf',
                  'bancada', 'nome_eleitoral', 'node_size')


class CoautoriaNodeList(generics.ListAPIView):
    '''
    Lista os nós
    '''
    serializer_class = CoautoriaNodeSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'id', openapi.IN_PATH, 'id da proposição no sistema',
                type=openapi.TYPE_INTEGER),
        ]
    )
    def get_queryset(self):
        id_prop = self.kwargs['id']
        return CoautoriaNode.objects.filter(id_leggo=id_prop)
