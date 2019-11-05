from rest_framework import serializers, generics
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.model.coautoria_edges import CoautoriaEdges


class CoautoriaEdgesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoautoriaEdges
        fields = ('source', 'target', 'value')


class CoautoriaEdgesList(generics.ListAPIView):
    '''
    Lista as arestas
    '''
    serializer_class = CoautoriaEdgesSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'id', openapi.IN_PATH, 'id da proposição no sistema',
                type=openapi.TYPE_INTEGER),
        ]
    )
    def get_queryset(self):
        id_prop = self.kwargs['id']
        return CoautoriaEdges.objects.filter(id_leggo=id_prop)
