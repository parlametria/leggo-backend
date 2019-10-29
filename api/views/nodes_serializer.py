from rest_framework import serializers, generics
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.model.nodes import Nodes


class NodesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nodes
        fields = ('id_autor', 'nome', 'partido', 'uf', 
        	'bancada', 'nome_eleitoral', 'node_size')

class NodesList(generics.ListAPIView):
    '''
    Lista os nós
    '''
    serializer_class = NodesSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'id', openapi.IN_PATH, 'id da proposição no sistema',
                type=openapi.TYPE_INTEGER),
        ]
    )
    def get_queryset(self):
        id_prop = self.kwargs['id']
        return Nodes.objects.filter(id_leggo=id_prop)